const token = () => document.querySelector('input[name="csrf_token"]')?.value || '';

// Navigation Toggle
document.querySelector('.menu')?.addEventListener('click', () => {
  document.querySelector('nav').classList.toggle('open');
});

// Theme Toggle
document.getElementById('theme-toggle')?.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});

// Split-Pane Editor and Test Runner Logic
document.querySelectorAll('.editor').forEach(editor => {
  const lang = editor.dataset.language;
  const isWeb = ['html-css', 'responsive-web-design'].includes(editor.dataset.course) && ['html', 'css'].includes(lang);
  const out = document.getElementById('console-output');
  const iframe = document.getElementById('live-preview');
  
  let pyodideReadyPromise = null;
  if (lang === 'python' && typeof loadPyodide !== 'undefined') {
    if (out) out.textContent = 'Loading Python environment (Pyodide). Please wait...';
    pyodideReadyPromise = loadPyodide().then(p => {
      if (out) out.textContent = 'Python environment ready.';
      return p;
    }).catch(err => {
      if (out) out.textContent = 'Failed to load Python environment: ' + err.message;
    });
  }

  // File Tabs
  const tabs = editor.querySelectorAll('.file-tab');
  const files = editor.querySelectorAll('.code-file[data-file]');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      files.forEach(f => f.classList.remove('active'));
      tab.classList.add('active');
      editor.querySelector(`.code-file[data-file="${tab.dataset.file}"]`).classList.add('active');
    });
  });

  const getCode = () => {
    if (isWeb) {
      const htmlEditor = document.getElementById('code-box-html');
      const previewMarkup = document.getElementById('preview-html')?.value || '';
      const html = htmlEditor?.value || previewMarkup;
      const cssEditor = document.getElementById('code-box-css');
      const css = cssEditor?.value || '';
      const htmlCode = html || '<!DOCTYPE html><html><body><h1>Practice preview</h1></body></html>';
      return { html: lang === 'css' ? css : html, css, full: `<style>${css}</style>\n${htmlCode}` };
    }
    return document.getElementById('code-box-main')?.value || '';
  };

  const runWebPreview = () => {
    if (!iframe) return;
    const { full } = getCode();
    iframe.srcdoc = full;
  };
  
  // Real-time update for web preview
  if (isWeb) {
    document.getElementById('code-box-html')?.addEventListener('input', runWebPreview);
    document.getElementById('code-box-css')?.addEventListener('input', runWebPreview);
    runWebPreview(); // initial render
  }

  editor.querySelector('.reset')?.addEventListener('click', () => {
    if (confirm('Are you sure you want to reset your code?')) {
      window.location.reload();
    }
  });

  // Client-Side Test Runner parsing the specific tests injected into the page
  const runLessonChecks = async (e) => {
    const btn = e.target;
    const lessonId = btn.dataset.lesson;
    const testResults = document.getElementById('test-results');
    const testList = document.getElementById('test-list');
    
    testResults.style.display = 'block';
    testList.innerHTML = '<li>Running tests...</li>';

    const filesCode = getCode();
    const code = isWeb ? filesCode.html : filesCode;
    const codeWithStyles = isWeb ? filesCode.full : code;

    // Read tests array
    let tests = [];
    try {
      const testJson = document.getElementById('lesson-tests')?.textContent || "[]";
      tests = JSON.parse(testJson);
    } catch (e) {
      console.error("Failed to parse tests", e);
    }

    let allPassed = true;
    let checks = [];

    // Run tests
    if (tests.length === 0) {
       // Fallback generic test if no specific tests provided
       if (code.trim().length > 0) checks.push({ passed: true, msg: "Code is not empty." });
       else { checks.push({ passed: false, msg: "Code cannot be empty." }); allPassed = false; }
    } else {
      if (lang === 'python' && pyodideReadyPromise) {
        // Evaluate python code first to load variables into Pyodide globals
        try {
          const pyodide = await pyodideReadyPromise;
          await pyodide.runPythonAsync(code);
          // Set globals for test execution (hacky but functional for prototype)
          window.pyodideVars = pyodide.globals.toJs();
        } catch (err) {
          checks.push({ passed: false, msg: "Python Execution Error: " + err.message });
          allPassed = false;
        }
      }

      for (let t of tests) {
        try {
          // Dangerous eval for tests, acceptable for client-side sandbox execution in educational platforms
          const passed = Function('code', 'fullCode', `return Boolean(${t.test});`)(code, codeWithStyles);
          checks.push({ passed, msg: t.message });
          if (!passed) allPassed = false;
        } catch (err) {
          checks.push({ passed: false, msg: `Test failed to execute: ${err.message}` });
          allPassed = false;
        }
      }
    }

    // Render results
    testList.innerHTML = '';
    checks.forEach(check => {
      const li = document.createElement('li');
      li.className = check.passed ? 'test-pass' : 'test-fail';
      li.textContent = (check.passed ? '✓ ' : '✗ ') + check.msg;
      testList.appendChild(li);
    });

    if (allPassed) {
      const li = document.createElement('li');
      li.style.color = '#10b981';
      li.style.marginTop = '10px';
      li.style.fontWeight = 'bold';
      li.textContent = 'All tests passed! Great job!';
      testList.appendChild(li);
      
      // Confetti!
      if (typeof confetti !== 'undefined') {
        confetti({
          particleCount: 150,
          spread: 70,
          origin: { y: 0.6 }
        });
      }

      // Hide the check button, show the Next Step button
      btn.style.display = 'none';
      const nextBtn = document.getElementById('next-lesson-btn');
      if (nextBtn) {
        nextBtn.style.display = 'block';
        btn.style.display = 'none';
      } else {
        await submitLesson(lessonId, btn);
      }
    } else {
      // Suggest AI hint on failure
      const li = document.createElement('li');
      li.style.marginTop = '10px';
      li.style.fontStyle = 'italic';
      li.textContent = 'Some tests failed. Ask the AI Tutor for a hint!';
      testList.appendChild(li);
    }
  };

  document.querySelector('.complete')?.addEventListener('click', runLessonChecks);
  document.getElementById('next-lesson-btn')?.addEventListener('click', (e) => {
    submitLesson(e.currentTarget.dataset.lesson, e.currentTarget);
  });

  editor.querySelectorAll('.code-file').forEach(codeInput => {
    codeInput.addEventListener('keydown', event => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        document.querySelector('.complete')?.click();
      }
    });
  });

});

async function submitLesson(lessonId, btn) {
  const originalText = btn.textContent;
  btn.disabled = true;
  btn.textContent = 'Saving progress…';
  try {
    const response = await fetch('/api/lessons/' + lessonId + '/complete', {
      method: 'POST',
      headers: { 'X-CSRFToken': token(), 'Accept': 'application/json' }
    });
    const result = await response.json().catch(() => ({}));
    if (response.status === 401 && result.login_url) {
      window.location.assign(result.login_url);
      return;
    }
    if (!response.ok || !result.ok) {
      throw new Error(result.error || 'Progress could not be saved. Please try again.');
    }
    window.location.assign(result.next_url || window.location.href);
  } catch (error) {
    btn.disabled = false;
    btn.textContent = originalText;
    alert(error.message || 'Could not save your lesson progress. Check your connection and try again.');
  }
}

// AI Chatbot Logic
const chatToggle = document.getElementById('ai-chat-toggle');
const chatBody = document.getElementById('ai-chat-body');
const chatContainer = document.getElementById('ai-chatbot');
let chatExpanded = true;

if (chatToggle) {
  chatToggle.addEventListener('click', () => {
    chatExpanded = !chatExpanded;
    if (chatExpanded) {
      chatBody.style.display = 'flex';
      document.getElementById('ai-chat-controls').style.display = 'block';
      chatToggle.textContent = '−';
    } else {
      chatBody.style.display = 'none';
      document.getElementById('ai-chat-controls').style.display = 'none';
      chatToggle.textContent = '+';
      chatContainer.style.width = '220px';
    }
    if (chatExpanded) chatContainer.style.width = '300px';
  });
}

document.getElementById('ai-hint-btn')?.addEventListener('click', () => {
  // Read hints from DOM
  let hints = [];
  try {
    hints = JSON.parse(document.getElementById('lesson-hints')?.textContent || "[]");
  } catch (e) {}

  if (hints.length === 0) {
    appendChatbotMessage("I don't have any specific hints for this lesson, but keep trying!");
    return;
  }

  // Get next hint
  const hintIndex = parseInt(chatContainer.dataset.hintIndex || "0");
  if (hintIndex < hints.length) {
    appendChatbotMessage("💡 Hint: " + hints[hintIndex]);
    chatContainer.dataset.hintIndex = hintIndex + 1;
  } else {
    appendChatbotMessage("You've seen all the hints! Try reviewing the lesson instructions again.");
  }
});

function appendChatbotMessage(text) {
  const div = document.createElement('div');
  div.className = 'ai-msg';
  div.style.background = 'rgba(38,119,255,0.1)';
  div.style.padding = '10px';
  div.style.borderRadius = '8px';
  div.style.fontSize = '13px';
  div.style.color = 'var(--ink)';
  div.textContent = text;
  
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Curriculum search
const courseSearch = document.getElementById('course-search');
if (courseSearch) {
  const filterLessons = () => {
    const query = courseSearch.value.trim().toLowerCase();
    const moduleCards = document.querySelectorAll('.curriculum details');

    moduleCards.forEach(card => {
      const rows = card.querySelectorAll('.lesson-row');
      let visible = 0;

      rows.forEach(row => {
        const match = !query || row.textContent.toLowerCase().includes(query);
        row.style.display = match ? 'flex' : 'none';
        if (match) visible += 1;
      });

      card.style.display = visible > 0 || !query ? 'block' : 'none';
    });
  };

  courseSearch.addEventListener('input', filterLessons);
}

// PWA
if ('serviceWorker' in navigator) navigator.serviceWorker.register('/static/sw.js');
