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

// FCC-style course map: open on desktop, use a closed drawer on narrow screens.
const lessonShell = document.getElementById('lesson-shell');
const sidebarToggle = document.getElementById('sidebar-toggle');
const sidebarScrim = document.getElementById('sidebar-scrim');
const sidebar = document.getElementById('lesson-sidebar');
const lessonViewport = window.matchMedia('(max-width: 960px)');
const setSidebarOpen = open => {
  if (!lessonShell || !sidebarToggle) return;
  lessonShell.classList.toggle('sidebar-closed', !open);
  sidebarToggle.setAttribute('aria-expanded', String(open));
  sidebarToggle.setAttribute('aria-label', open ? 'Hide course steps' : 'Show course steps');
  if (sidebar) sidebar.inert = !open;
};
if (lessonShell && sidebarToggle) {
  setSidebarOpen(!lessonViewport.matches);
  sidebarToggle.addEventListener('click', () => setSidebarOpen(lessonShell.classList.contains('sidebar-closed')));
  sidebarScrim?.addEventListener('click', () => setSidebarOpen(false));
  sidebar?.querySelectorAll('.sidebar-step').forEach(step => {
    step.addEventListener('click', () => {
      if (lessonViewport.matches) setSidebarOpen(false);
    });
  });
  lessonViewport.addEventListener('change', event => setSidebarOpen(!event.matches));
}

// Progressive lesson hints, kept behind a small help button to avoid clutter.
const hintFab = document.getElementById('hint-fab-btn');
const hintPanel = document.getElementById('hint-panel');
const hintText = document.getElementById('hint-text');
const hintClose = document.getElementById('hint-close-btn');
const hintNext = document.getElementById('hint-next-btn');
let lessonHints = [];
let hintIndex = 0;
try {
  lessonHints = JSON.parse(document.getElementById('lesson-hints')?.textContent || '[]');
} catch (_) {
  lessonHints = [];
}
const showHint = () => {
  if (!hintPanel || !hintText) return;
  if (!lessonHints.length) {
    hintText.textContent = 'No hint is available for this step yet. Re-read the task and check one small detail at a time.';
    if (hintNext) hintNext.hidden = true;
  } else {
    hintText.textContent = lessonHints[Math.min(hintIndex, lessonHints.length - 1)];
    hintIndex = Math.min(hintIndex + 1, lessonHints.length - 1);
    if (hintNext) hintNext.hidden = hintIndex >= lessonHints.length - 1;
  }
  hintPanel.hidden = false;
};
hintFab?.addEventListener('click', showHint);
hintClose?.addEventListener('click', () => { if (hintPanel) hintPanel.hidden = true; });
hintNext?.addEventListener('click', showHint);

// Split-Pane Editor and Test Runner Logic
document.querySelectorAll('.editor').forEach(editor => {
  const lang = editor.dataset.language;
  const draftKey = `codeforge:draft:${editor.dataset.draftKey}`;
  const isWeb = ['html-css', 'responsive-web-design'].includes(editor.dataset.course) && ['html', 'css'].includes(lang);
  const out = document.getElementById('console-output');
  const iframe = document.getElementById('live-preview');
  const draftStatus = document.getElementById('draft-status');
  const codeInputs = [...editor.querySelectorAll('.code-file')];
  let serverDraft = {};
  try {
    serverDraft = JSON.parse(document.getElementById('lesson-saved-draft')?.textContent || 'null') || {};
    codeInputs.forEach(input => {
      if (Object.hasOwn(serverDraft, input.dataset.file)) input.value = serverDraft[input.dataset.file];
    });
    if (Object.keys(serverDraft).length && draftStatus) draftStatus.textContent = 'Account draft restored';
  } catch (error) {
    serverDraft = {};
  }

  try {
    const savedDraft = localStorage.getItem(draftKey);
    if (savedDraft && Object.keys(serverDraft).length === 0) {
      const draft = JSON.parse(savedDraft);
      codeInputs.forEach(input => {
        if (Object.hasOwn(draft, input.dataset.file)) input.value = draft[input.dataset.file];
      });
      if (draftStatus) draftStatus.textContent = 'Draft restored';
    }
  } catch (error) {
    if (draftStatus) draftStatus.textContent = 'Draft storage unavailable';
  }

  let serverSaveTimer;
  const saveDraft = () => {
    try {
      const draft = Object.fromEntries(codeInputs.map(input => [input.dataset.file, input.value]));
      localStorage.setItem(draftKey, JSON.stringify(draft));
      if (draftStatus) draftStatus.textContent = 'Saved on this device';
      const saveUrl = editor.dataset.saveDraftUrl;
      if (saveUrl) {
        window.clearTimeout(serverSaveTimer);
        serverSaveTimer = window.setTimeout(async () => {
          try {
            const response = await fetch(saveUrl, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token(), 'Accept': 'application/json' },
              body: JSON.stringify({ draft })
            });
            if (response.ok && draftStatus) draftStatus.textContent = 'Saved to your account';
          } catch (error) {
            if (draftStatus) draftStatus.textContent = 'Saved on this device';
          }
        }, 700);
      }
    } catch (error) {
      if (draftStatus) draftStatus.textContent = 'Could not save draft';
    }
  };
  codeInputs.forEach(input => input.addEventListener('input', saveDraft));
  
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
      const html = htmlEditor ? htmlEditor.value : previewMarkup;
      const cssEditor = document.getElementById('code-box-css');
      const css = cssEditor ? cssEditor.value : '';
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
      codeInputs.forEach(input => { input.value = ''; });
      try { localStorage.removeItem(draftKey); } catch (error) {}
      if (editor.dataset.saveDraftUrl) {
        fetch(editor.dataset.saveDraftUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token(), 'Accept': 'application/json' },
          body: JSON.stringify({ draft: Object.fromEntries(codeInputs.map(input => [input.dataset.file, input.value])) })
        }).catch(() => {});
      }
      if (draftStatus) draftStatus.textContent = 'Draft cleared';
      if (isWeb) runWebPreview();
    }
  });

  // Client-Side Test Runner parsing the specific tests injected into the page
  const runLessonChecks = async (e) => {
    const btn = e.currentTarget;
    const lessonId = btn.dataset.lesson;
    const testList = document.getElementById('test-list');
    if (!testList) return;
    testList.replaceChildren();
    const running = document.createElement('p');
    running.className = 'test-panel-placeholder';
    running.textContent = 'Running tests…';
    testList.appendChild(running);

    const filesCode = getCode();
    const code = isWeb ? (lang === 'css' ? filesCode.css : filesCode.html) : filesCode;
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
    testList.replaceChildren();
    checks.forEach(check => {
      const row = document.createElement('div');
      row.className = `test-item ${check.passed ? 'pass' : 'fail'}`;
      const icon = document.createElement('span');
      icon.className = 'test-item-icon';
      icon.setAttribute('aria-hidden', 'true');
      icon.textContent = check.passed ? '✓' : '✗';
      const message = document.createElement('span');
      message.textContent = check.msg;
      row.append(icon, message);
      testList.appendChild(row);
    });

    if (allPassed) {
      const success = document.createElement('p');
      success.className = 'test-all-pass';
      success.textContent = '✓ All tests passed! Great job.';
      testList.appendChild(success);
      
      // Confetti!
      celebrate();

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
      const guidance = document.createElement('p');
      guidance.className = 'test-guidance';
      guidance.textContent = 'Some tests failed. Review the steps and try again, or use a hint.';
      testList.appendChild(guidance);
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

function celebrate() {
  if (typeof confetti !== 'undefined') {
    confetti({ particleCount: 150, spread: 80, origin: { y: 0.62 } });
    return;
  }

  const colors = ['#2677ff', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'];
  for (let index = 0; index < 80; index += 1) {
    const piece = document.createElement('span');
    piece.className = 'confetti-piece';
    piece.style.left = `${Math.random() * 100}vw`;
    piece.style.backgroundColor = colors[index % colors.length];
    piece.style.setProperty('--fall-duration', `${1.5 + Math.random() * 1.6}s`);
    piece.style.setProperty('--spin', `${Math.random() * 900 - 450}deg`);
    document.body.appendChild(piece);
    window.setTimeout(() => piece.remove(), 3300);
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

// Installable/offline course PWA
let installPromptEvent = null;
const installButton = document.getElementById('install-app');
window.addEventListener('beforeinstallprompt', event => {
  event.preventDefault();
  installPromptEvent = event;
  if (installButton) installButton.hidden = false;
});
installButton?.addEventListener('click', async () => {
  if (!installPromptEvent) return;
  installPromptEvent.prompt();
  await installPromptEvent.userChoice;
  installPromptEvent = null;
  installButton.hidden = true;
});
window.addEventListener('appinstalled', () => {
  installPromptEvent = null;
  if (installButton) installButton.hidden = true;
});
if ('serviceWorker' in navigator) navigator.serviceWorker.register('/sw.js', { scope: '/' });
