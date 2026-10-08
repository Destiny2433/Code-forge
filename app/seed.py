import json
import os

from . import db
from .models import Course, Lesson, Module, User


def build_lesson(title, slug, body, example_code, code, language="html", tests=None, hints=None):
    return {
        "title": title,
        "slug": slug,
        "body": body,
        "example_code": example_code,
        "code": code,
        "language": language,
        "tests": json.dumps(tests or [
            {"test": "code.length > 0", "message": "Keep building the lesson and use the example as your guide."}
        ]),
        "hints": json.dumps(hints or [
            "Review the example code.",
            "Use the lesson goal to guide your structure.",
            "Test your code and refine your solution."
        ]),
    }


def seed():
    """Create the full responsive web design curriculum based on the requested learning roadmap."""
    catalog = [
        {
            "title": "Responsive Web Design Certification",
            "slug": "responsive-web-design",
            "description": "This course teaches the fundamentals of HTML and CSS, including modern layout, design, accessibility, and responsive web development. You'll build practical projects and gain the skills to create professional, user-friendly webpages.",
            "modules": [
                {
                    "title": "Basic HTML",
                    "lessons": [
                        build_lesson(
                            "HTML from Scratch: Your First Webpage",
                            "html-from-scratch-your-first-webpage",
                            "<p><strong>What you will learn:</strong> HTML is the language browsers use to understand webpage content. It is like the labeled frame of a house: HTML says what is a heading, paragraph, image, or link; CSS decorates it later.</p><p><strong>Why it matters:</strong> clear HTML makes a page understandable to browsers, search engines, and assistive technology. HTML is not a programming language; it describes the structure and meaning of content.</p><p><strong>Your task:</strong> make a tiny page with a main heading and a paragraph. The browser preview on the right updates as you type.</p>",
                            "<!DOCTYPE html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"UTF-8\">\n    <title>My First Page</title>\n  </head>\n  <body>\n    <h1>Hello, web!</h1>\n    <p>I am learning HTML.</p>\n  </body>\n</html>",
                            "<!DOCTYPE html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"UTF-8\">\n    <title>My First Page</title>\n  </head>\n  <body>\n    <h1>My first page</h1>\n  </body>\n</html>",
                            tests=[
                                {"test": "code.includes('<!DOCTYPE html>')", "message": "Start with the HTML doctype."},
                                {"test": "code.includes('<h1') && code.includes('</h1>')", "message": "Add a complete main heading using h1."},
                                {"test": "code.includes('<p') && code.includes('</p>')", "message": "Add a complete paragraph using p."}
                            ],
                            hints=["Keep the existing page skeleton.", "Add a <p> sentence inside <body>.", "A paragraph needs both <p> and </p> tags."]
                        ),
                        build_lesson(
                            "HTML Elements: Opening Tags, Content, and Closing Tags",
                            "html-elements-opening-and-closing-tags",
                            "<p><strong>Understand it:</strong> most HTML elements have an opening tag, content, and a closing tag. In <code>&lt;p&gt;Hello&lt;/p&gt;</code>, the tags mark the paragraph boundaries and Hello is its content. Tags are instructions; the words between them are what visitors read.</p><p><strong>Watch for this:</strong> forgetting a closing tag can cause the browser to treat later content as part of the same element.</p><p><strong>Your task:</strong> add a second paragraph that tells visitors what you are learning.</p>",
                            "<h1>My learning page</h1>\n<p>I am learning HTML.</p>\n<p>HTML gives content structure.</p>",
                            "<h1>My learning page</h1>\n<p>I am learning HTML.</p>",
                            tests=[
                                {"test": "(code.match(/<p\\b/g) || []).length >= 2", "message": "Add a second paragraph element."},
                                {"test": "(code.match(/<\\/p>/g) || []).length >= 2", "message": "Close both paragraph elements."}
                            ],
                            hints=["Add a new line after your current paragraph.", "Start it with <p> and finish with </p>.", "Put your own sentence between those tags."]
                        ),
                        build_lesson(
                            "Headings: Give Your Page a Clear Outline",
                            "html-headings-page-outline",
                            "<p><strong>Understand it:</strong> headings create an outline. Use one main <code>&lt;h1&gt;</code> for the page topic, then <code>&lt;h2&gt;</code> for major sections. A heading level describes importance, not just how large text should look.</p><p><strong>Why it matters:</strong> a logical heading outline helps visitors scan the page and helps screen-reader users navigate it.</p><p><strong>Your task:</strong> add an h2 section heading under the page title.</p>",
                            "<h1>My Favorite Things</h1>\n<h2>Books</h2>\n<p>I enjoy adventure stories.</p>",
                            "<h1>My Favorite Things</h1>\n<p>I enjoy adventure stories.</p>",
                            tests=[
                                {"test": "code.includes('<h1') && code.includes('</h1>')", "message": "Keep one main h1 heading."},
                                {"test": "code.includes('<h2') && code.includes('</h2>')", "message": "Add a section heading using h2."}
                            ],
                            hints=["Keep the h1 as the page title.", "Add <h2>Books</h2> below it.", "Put the paragraph after the section heading."]
                        ),
                        build_lesson(
                            "Paragraphs and Text Emphasis",
                            "html-paragraphs-and-text-emphasis",
                            "<p><strong>Understand it:</strong> use <code>&lt;p&gt;</code> for a block of prose. Use <code>&lt;strong&gt;</code> when text is especially important and <code>&lt;em&gt;</code> when it deserves emphasis. These tags communicate meaning, not only visual style.</p><p><strong>Your task:</strong> write a paragraph and emphasize the most important word with strong.</p>",
                            "<p>Practice a little every day and <strong>keep going</strong>.</p>",
                            "<p>Practice a little every day.</p>",
                            tests=[
                                {"test": "code.includes('<p') && code.includes('</p>')", "message": "Write a complete paragraph."},
                                {"test": "code.includes('<strong>') && code.includes('</strong>')", "message": "Emphasize an important word with strong."}
                            ],
                            hints=["Put your sentence inside a paragraph.", "Wrap an important word with <strong> and </strong>."]
                        ),
                        build_lesson(
                            "Links: Connect Pages and Places",
                            "html-links-href",
                            "<p><strong>Understand it:</strong> an anchor element creates a link. Its <code>href</code> attribute stores the destination; the text between the tags tells people where the link goes.</p><p><strong>Example:</strong> <code>&lt;a href=\"https://example.com\"&gt;Visit Example&lt;/a&gt;</code>.</p><p><strong>Your task:</strong> add a link to a website you like. Use a clear, descriptive link label.</p>",
                            "<a href=\"https://example.com\">Visit Example</a>",
                            "<p>My favorite resource is <a href=\"https://example.com\">Example</a>.</p>",
                            tests=[
                                {"test": "code.includes('<a ') && code.includes('href=')", "message": "Add a link with an href destination."},
                                {"test": "code.includes('</a>')", "message": "Close the anchor element after its link text."}
                            ],
                            hints=["Start a link with <a href=\"...\">.", "Put readable link text between the tags.", "Close the link with </a>."]
                        ),
                        build_lesson(
                            "Images: Sources and Useful Alternative Text",
                            "html-images-and-alt-text",
                            "<p><strong>Understand it:</strong> an image uses <code>&lt;img&gt;</code>. The <code>src</code> attribute points to the image file. The <code>alt</code> attribute describes its useful content for someone who cannot see it. An image is a void element, so it does not need a closing tag.</p><p><strong>Your task:</strong> add an image with a source and a meaningful alt description. You can use <code>photo.jpg</code> as a sample filename.</p>",
                            "<img src=\"photo.jpg\" alt=\"A red bicycle leaning beside a tree\">",
                            "<img src=\"photo.jpg\" alt=\"A red bicycle\">",
                            tests=[
                                {"test": "code.includes('<img') && code.includes('src=')", "message": "Add an image with a source."},
                                {"test": "code.includes('alt=')", "message": "Describe the image with alt text."}
                            ],
                            hints=["Add an <img> tag.", "Use src=\"photo.jpg\" for the image path.", "Add alt=\"...\" that describes the image."]
                        ),
                        build_lesson(
                            "Lists: Organize Related Items",
                            "html-lists-ul-ol-li",
                            "<p><strong>Understand it:</strong> use <code>&lt;ul&gt;</code> for a list where order does not matter and <code>&lt;ol&gt;</code> when order does matter. Each item belongs inside an <code>&lt;li&gt;</code> element.</p><p><strong>Your task:</strong> make an unordered list of three things you want to learn.</p>",
                            "<ul>\n  <li>HTML</li>\n  <li>CSS</li>\n  <li>Accessibility</li>\n</ul>",
                            "<ul>\n  <li>HTML</li>\n</ul>",
                            tests=[
                                {"test": "code.includes('<ul') && code.includes('</ul>')", "message": "Create a complete unordered list."},
                                {"test": "(code.match(/<li\\b/g) || []).length >= 3", "message": "Add at least three list items."}
                            ],
                            hints=["Keep all items between <ul> and </ul>.", "Each list item starts with <li> and ends with </li>.", "Add two more list items."]
                        ),
                        build_lesson(
                            "Semantic HTML: Describe the Purpose of Each Region",
                            "html-semantic-page-structure",
                            "<p><strong>Understand it:</strong> semantic elements describe what a region does. <code>&lt;header&gt;</code> introduces a page or section, <code>&lt;main&gt;</code> contains its primary content, and <code>&lt;footer&gt;</code> contains closing information.</p><p><strong>Why it matters:</strong> meaningful structure helps browsers, search engines, and assistive technology understand the page.</p><p><strong>Your task:</strong> place your main heading in a header and your main content in a main element.</p>",
                            "<header><h1>My Portfolio</h1></header>\n<main><p>Welcome to my work.</p></main>\n<footer><p>Made by me.</p></footer>",
                            "<header><h1>My Portfolio</h1></header>\n<main><p>Welcome to my work.</p></main>",
                            tests=[
                                {"test": "code.includes('<header') && code.includes('</header>')", "message": "Add a complete header region."},
                                {"test": "code.includes('<main') && code.includes('</main>')", "message": "Add a complete main content region."}
                            ],
                            hints=["Use header for the page introduction.", "Put the main content inside <main> and </main>.", "The footer is optional for this task."]
                        ),
                        build_lesson("Build a Curriculum Outline", "build-a-curriculum-outline", "Organize a learning plan and structure the content in a clear sequence.", "<section>\n  <h1>Web Development Curriculum</h1>\n  <ul>\n    <li>HTML</li>\n    <li>CSS</li>\n    <li>Responsive Design</li>\n  </ul>\n</section>", "<section>\n  <h1>Web Development Curriculum</h1>\n</section>"),
                        build_lesson("Debug Camperbot's Profile Page", "debug-camperbots-profile-page", "Practice spotting structure and content issues in a simple profile page.", "<article>\n  <h1>Camperbot</h1>\n  <p>Frontend learner and creative problem solver.</p>\n</article>", "<article>\n  <h1>Camperbot</h1>\n</article>"),
                        build_lesson("Understanding HTML Attributes", "understanding-html-attributes", "HTML attributes add meaning and behavior to elements. Use them carefully and consistently.", "<img src=\"sunset.jpg\" alt=\"A warm sunset\" width=\"300\">\n<a href=\"https://example.com\">Visit</a>", "<img src=\"sunset.jpg\" alt=\"A warm sunset\">\n<a href=\"https://example.com\">Visit</a>"),
                        build_lesson("Debug a Pet Adoption Page", "debug-a-pet-adoption-page", "Fix the structure and improve the readability of a pet adoption landing page.", "<main>\n  <h1>Adopt a Companion</h1>\n  <p>Find a pet that fits your lifestyle.</p>\n</main>", "<main>\n  <h1>Adopt a Companion</h1>\n</main>"),
                        build_lesson("Understanding the HTML Boilerplate", "understanding-the-html-boilerplate", "Set up the document correctly so browsers can render your page as intended.", "<!DOCTYPE html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"UTF-8\">\n    <title>CodeForge</title>\n  </head>\n  <body>\n    <h1>Welcome to CodeForge</h1>\n  </body>\n</html>", "<!DOCTYPE html>\n<html lang=\"en\">\n  <head>\n    <title>CodeForge</title>\n  </head>\n  <body>\n    <h1>Welcome</h1>\n  </body>\n</html>"),
                        build_lesson("Build a Cat Photo App", "build-a-cat-photo-app", "Structure a fun, content-rich page using headings, paragraphs, links, and images.", "<h1>CatPhotoApp</h1>\n<h2>Cat Photos</h2>\n<p>See more cat photos in our gallery.</p>", "<h1>Hello World</h1>\n"),
                        build_lesson("Build a Recipe Page", "build-a-recipe-page", "Create a recipe layout with clear headings and readable content sections.", "<h1>Easy Pancakes</h1>\n<h2>Ingredients</h2>\n<ul>\n  <li>Flour</li>\n  <li>Milk</li>\n</ul>", "<h1>Easy Pancakes</h1>\n"),
                        build_lesson("HTML Fundamentals", "html-fundamentals", "Review the core rules for semantic structure, content flow, and page organization.", "<header>\n  <h1>CodeForge</h1>\n</header>\n<main>\n  <p>Build a strong base with semantic HTML.</p>\n</main>", "<header>\n  <h1>CodeForge</h1>\n</header>\n"),
                        build_lesson("Build a Bookstore Page", "build-a-bookstore-page", "Design a bookstore landing page with clear sections and call-to-action content.", "<section>\n  <h1>Open Book Store</h1>\n  <p>Discover your next favorite read.</p>\n</section>", "<section>\n  <h1>Open Book Store</h1>\n</section>"),
                        build_lesson("Understanding How HTML Affects SEO", "understanding-how-html-affects-seo", "Learn how headings, metadata, and meaningful structure affect search visibility.", "<title>CodeForge Blog</title>\n<meta name=\"description\" content=\"Learn front-end development with practical lessons.\">", "<title>CodeForge Blog</title>\n"),
                        build_lesson("Build a Travel Agency Page", "build-a-travel-agency-page", "Create a clear service landing page with a hero section and useful information blocks.", "<section class=\"hero\">\n  <h1>Explore the world</h1>\n  <p>Build unforgettable travel memories.</p>\n</section>", "<section class=\"hero\">\n  <h1>Explore the world</h1>\n</section>"),
                        build_lesson("Working with Audio and Video Elements", "working-with-audio-and-video-elements", "Use media elements to enrich content and improve the storytelling experience on your page.", "<video controls src=\"demo.mp4\"></video>\n<audio controls src=\"demo.mp3\"></audio>", "<video controls></video>\n"),
                        build_lesson("Build an HTML Music Player", "build-an-html-music-player", "Create a simple player interface with media controls and descriptive labels.", "<audio controls>\n  <source src=\"song.mp3\" type=\"audio/mpeg\">\n</audio>", "<audio controls></audio>"),
                        build_lesson("Build an HTML Video Player", "build-an-html-video-player", "Practice embedding and styling a video element within a content area.", "<video controls width=\"640\">\n  <source src=\"movie.mp4\" type=\"video/mp4\">\n</video>", "<video controls></video>"),
                        build_lesson("Build an HTML Audio and Video Player", "build-an-html-audio-and-video-player", "Combine multiple media components into a rich multimedia layout.", "<section>\n  <h2>Media Player</h2>\n  <audio controls></audio>\n  <video controls></video>\n</section>", "<section>\n  <h2>Media Player</h2>\n</section>"),
                        build_lesson("Working with Images and SVGs", "working-with-images-and-svgs", "Use vector and raster graphics to add visual depth to your layouts.", "<img src=\"cat.jpg\" alt=\"Cat sitting in sunlight\">\n<svg viewBox=\"0 0 100 100\"><circle cx=\"50\" cy=\"50\" r=\"40\" /></svg>", "<img src=\"cat.jpg\" alt=\"Cat sitting in sunlight\">"),
                        build_lesson("Build a Heart Icon", "build-a-heart-icon", "Create a simple SVG-based icon that can scale without losing quality.", "<svg viewBox=\"0 0 100 100\" aria-label=\"Heart icon\">\n  <path d=\"M50 85 L14 50 Q8 20 40 20 Q55 20 50 35 Q45 20 60 20 Q92 20 86 50 Z\" fill=\"red\"/>\n</svg>", "<svg viewBox=\"0 0 100 100\"></svg>"),
                        build_lesson("Working with the iframe Element", "working-with-the-iframe-element", "Embed external content contextually and thoughtfully in your page structure.", "<iframe src=\"https://example.com\" title=\"Example website\" width=\"600\" height=\"400\"></iframe>", "<iframe src=\"https://example.com\" title=\"Example website\"></iframe>"),
                        build_lesson("Build a Video Display Using iframe", "build-a-video-display-using-iframe", "Create an embedded content block using an iframe.", "<iframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/dQw4w9WgXcQ\" title=\"Video demo\"></iframe>", "<iframe title=\"Video demo\"></iframe>"),
                        build_lesson("Build a Video Compilation Page", "build-a-video-compilation-page", "Organize multiple videos into a simple showcase page.", "<section>\n  <h2>Video Collection</h2>\n  <iframe src=\"https://example.com\"></iframe>\n</section>", "<section>\n  <h2>Video Collection</h2>\n</section>"),
                        build_lesson("Working with Links", "working-with-links", "Design meaningful navigation and call-to-action links for the user journey.", "<nav>\n  <a href=\"#home\">Home</a>\n  <a href=\"#about\">About</a>\n  <a href=\"#contact\">Contact</a>\n</nav>", "<nav>\n  <a href=\"#home\">Home</a>\n</nav>"),
                        build_lesson("Basic HTML Review", "basic-html-review", "Summarize the key HTML rules and revisit the most important concepts.", "<article>\n  <h1>HTML Review</h1>\n  <p>Semantic structure, media, and clear content flow matter.</p>\n</article>", "<article>\n  <h1>HTML Review</h1>\n</article>"),
                        build_lesson("Basic HTML Quiz", "basic-html-quiz", "Check your understanding of the foundational HTML concepts you have covered.", "<form>\n  <label>Q: What does HTML structure?</label>\n  <input type=\"text\" value=\"content\">\n</form>", "<form>\n  <label>Question</label>\n</form>"),
                    ],
                },
                {
                    "title": "Semantic HTML",
                    "lessons": [
                        build_lesson("Semantic HTML Fundamentals", "semantic-html-fundamentals", "Use semantic elements to make content easier for humans and machines to understand.", "<header><nav>Home</nav></header><main><article><h2>Latest</h2></article></main>", "<header><nav>Home</nav></header>"),
                        build_lesson("Structuring Accessible Content", "structuring-accessible-content", "Create document structure that helps both readers and assistive technology.", "<section><h2>Services</h2><p>We design exciting user experiences.</p></section>", "<section><h2>Services</h2></section>"),
                        build_lesson("Using article, section, and aside", "using-article-section-and-aside", "Organize content into meaningful blocks for readability and structure.", "<article><h2>Case Study</h2><p>Results improved after redesign.</p></article><aside><p>Share this article</p></aside>", "<article><h2>Case Study</h2></article>"),
                    ],
                },
                {
                    "title": "Forms and Tables",
                    "lessons": [
                        build_lesson("Build a Survey Form", "build-a-survey-form", "Collect user input with accessible labels and organized form controls.", "<form>\n  <label for=\"name\">Name</label>\n  <input id=\"name\" type=\"text\">\n  <button type=\"submit\">Send</button>\n</form>", "<form>\n  <input type=\"text\">\n</form>"),
                        build_lesson("Create Structured Tables", "create-structured-tables", "Present data clearly using table rows, headers, and captions.", "<table>\n  <caption>Course schedule</caption>\n  <tr><th>Course</th><th>Time</th></tr>\n</table>", "<table>\n  <tr><th>Course</th></tr>\n</table>"),
                        build_lesson("Accessible Form Best Practices", "accessible-form-best-practices", "Improve form usability with labels, grouping, and clear validation states.", "<fieldset>\n  <legend>Account</legend>\n  <label>Email</label>\n  <input type=\"email\">\n</fieldset>", "<fieldset>\n  <legend>Account</legend>\n</fieldset>"),
                    ],
                },
                {
                    "title": "Accessibility",
                    "lessons": [
                        build_lesson("Accessibility Fundamentals", "accessibility-fundamentals", "Build interfaces that are easier for everyone to understand and use.", "<img src=\"cat.jpg\" alt=\"Black cat sitting near a window\">\n<label for=\"email\">Email</label>", "<img src=\"cat.jpg\" alt=\"Black cat\">"),
                        build_lesson("Alt Text and Labels", "alt-text-and-labels", "Use textual descriptions and form labels to improve clarity and usability.", "<label for=\"search\">Search</label>\n<input id=\"search\" type=\"search\">", "<label>Search</label>\n<input type=\"search\">"),
                        build_lesson("Color Contrast and Readability", "color-contrast-and-readability", "Use contrast and spacing carefully to make content easier to read.", "<p class=\"note\">This is readable text with good contrast.</p>", "<p class=\"note\">Readable text</p>"),
                    ],
                },
                {
                    "title": "HTML Review",
                    "lessons": [
                        build_lesson("HTML Review", "html-review", "Combine your understanding of structure, forms, media, and semantics into one strong foundation.", "<main><header><h1>HTML Review</h1></header><section><p>Keep it semantic.</p></section></main>", "<main><header><h1>HTML Review</h1></header></main>"),
                    ],
                },
                {
                    "title": "Computer Basics",
                    "lessons": [
                        build_lesson("Understanding Computer, Internet, and Tooling Basics", "understanding-computer-internet-and-tooling-basics", "Get comfortable with key tools, digital workflows, and how the web works.", "<p>Computers help developers write, test, and ship code.</p>", "<p>Computers are useful tools.</p>"),
                        build_lesson("What Are the Basic Parts of a Computer?", "what-are-the-basic-parts-of-a-computer", "Learn the major hardware and software pieces used in everyday development work.", "<ul><li>CPU</li><li>RAM</li><li>Storage</li><li>Keyboard</li></ul>", "<ul><li>CPU</li></ul>"),
                        build_lesson("How Can You Effectively Work With Your Keyboard, Mouse, and Other Pointing Devices?", "how-can-you-effectively-work-with-keyboard-mouse-and-pointers", "Learn keyboard shortcuts and efficient input habits that speed up development.", "<p>Use shortcuts and proper mouse movement to work faster.</p>", "<p>Use shortcuts.</p>"),
                        build_lesson("What Are the Different Types of Internet Service Providers?", "what-are-the-different-types-of-internet-service-providers", "Understand how internet access is delivered and what options exist.", "<ul><li>Fiber</li><li>Cable</li><li>DSL</li><li>Satellite</li></ul>", "<ul><li>Fiber</li></ul>"),
                        build_lesson("What Are Safe Ways to Sign Into Your Computer?", "what-are-safe-ways-to-sign-into-your-computer", "Practice good security habits when accessing your machine and accounts.", "<p>Use a PIN, password, and secure device login.</p>", "<p>Use secure login habits.</p>"),
                        build_lesson("What Are the Different Types of Tools Professional Developers Use?", "what-are-the-different-types-of-tools-professional-developers-use", "Recognize the software and workflows used to build, debug, and deploy apps.", "<ul><li>Text editor</li><li>Terminal</li><li>Browser</li><li>Version control</li></ul>", "<ul><li>Text editor</li></ul>"),
                    ],
                },
                {
                    "title": "Working with File Systems",
                    "lessons": [
                        build_lesson("How Can You Use File Management Applications on Your Computer?", "how-can-you-use-file-management-applications-on-your-computer", "Understand how to organize and manage files on your computer effectively.", "<ul><li>Open folders</li><li>Rename files</li><li>Move content</li></ul>", "<ul><li>Open folders</li></ul>"),
                        build_lesson("What Are Best Practices for Naming Files for Web Applications?", "best-practices-for-naming-files", "Use clean, consistent naming conventions to keep a project maintainable.", "<p>Use lowercase names and clear, descriptive filenames.</p>", "<p>Use meaningful names.</p>"),
                        build_lesson("What Are Best Practices for File and Folder Organization in Web Applications?", "best-practices-for-file-and-folder-organization", "Keep project folders clear, structured, and easy to navigate.", "<ul><li>src</li><li>assets</li><li>styles</li><li>docs</li></ul>", "<ul><li>src</li></ul>"),
                        build_lesson("How Can You Create, Move, and Delete Files and Folders Using Explorer or Finder?", "create-move-and-delete-files-and-folders", "Practice the basic file operations needed in web development workflows.", "<p>Create, move, rename, and delete digital assets intentionally.</p>", "<p>Organize your files carefully.</p>"),
                        build_lesson("How Can You Search for Files and Folders on Your Computer?", "search-for-files-and-folders-on-your-computer", "Use search tools to find assets quickly during real projects.", "<p>Use search filters and folder navigation to locate project files efficiently.</p>", "<p>Search smartly.</p>"),
                        build_lesson("What Are Some Common File Types You Will Work With in Web Applications?", "common-file-types-you-work-with", "Learn the common formats used in HTML, CSS, JavaScript, and images.", "<ul><li>.html</li><li>.css</li><li>.js</li><li>.png</li></ul>", "<ul><li>.html</li></ul>"),
                    ],
                },
                {
                    "title": "Browsing the Web Effectively",
                    "lessons": [
                        build_lesson("What Are the Common Web Browsers Available Today and How Do You Install One?", "common-web-browsers-and-how-to-install-one", "Use browser tools and browser choice to test and validate your work.", "<ul><li>Chrome</li><li>Edge</li><li>Firefox</li><li>Safari</li></ul>", "<ul><li>Chrome</li></ul>"),
                        build_lesson("What Is the Difference Between a Web Browser, a Website, and a Search Engine?", "difference-between-browser-website-and-search-engine", "Clarify the difference between browsing, websites, and information discovery.", "<p>A browser renders the website; a search engine helps you discover it.</p>", "<p>Browsers render pages.</p>"),
                        build_lesson("How to Use a Search Engine Effectively to Achieve Optimal Results", "how-to-use-search-engine-effectively", "Search with clear terms and use resources strategically to solve problems.", "<p>Use targeted search queries and verify trustworthy sources.</p>", "<p>Search efficiently.</p>"),
                        build_lesson("Computer Basics Review", "computer-basics-review", "Review the key ideas behind computing, tooling, and file management.", "<section><h2>Computer Basics Review</h2><p>Good workflow habits improve your development speed.</p></section>", "<section><h2>Computer Basics Review</h2></section>"),
                        build_lesson("Computer Basics Quiz", "computer-basics-quiz", "Test how well you understand the foundations of modern development workflows.", "<form><label>What is the browser used for?</label><input type=\"text\"></form>", "<form><label>Question</label></form>"),
                    ],
                },
                {
                    "title": "Basic CSS",
                    "lessons": [
                        build_lesson("What Is CSS?", "what-is-css", "CSS controls visual design, spacing, and layout on the page.", "body { font-family: Arial, sans-serif; background: #f5f7fb; }\nh1 { color: #2563eb; }", "body { background: #f5f7fb; }\nh1 { color: blue; }"),
                        build_lesson("What Is the Basic Anatomy of a CSS Rule?", "basic-anatomy-of-a-css-rule", "Understand selectors, declarations, and property-value pairs.", ".card { color: #111827; padding: 16px; }", ".card { color: #111827; }"),
                        build_lesson("What Is the Meta Viewport Element Used For?", "meta-viewport-element", "Control mobile layout scaling with the viewport meta tag.", "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">", "<meta name=\"viewport\" content=\"width=device-width\">"),
                        build_lesson("What Are Some Default Browser Styles Applied to HTML?", "default-browser-styles", "Recognize how browsers add default styling to headings and lists.", "h1 { font-size: 2em; }\np { margin-block: 1em; }", "h1 { font-size: 2em; }"),
                        build_lesson("What Are Inline, Internal, and External CSS, and When Should You Use Each One?", "inline-internal-and-external-css", "Choose the right CSS approach based on the scope and purpose of your styling.", "<style>body { color: #111827; }</style>\n<p style=\"color: blue\">Blue text</p>", "<style>body { color: #111827; }</style>"),
                        build_lesson("How Do Width and Height Work?", "how-do-width-and-height-work", "Understand the default sizing model and how content boxes are measured.", ".box { width: 240px; height: 120px; }", ".box { width: 240px; }"),
                        build_lesson("What Are the Different Types of CSS Combinators?", "css-combinators", "Learn how descendant, child, and adjacent selectors target elements.", "section > h2 { color: #2563eb; }\ndiv p { margin-bottom: 1rem; }", "section > h2 { color: #2563eb; }"),
                        build_lesson("What Is the Difference Between Inline and Block-Level Elements in CSS?", "difference-between-inline-and-block-level-elements", "Understand layout behavior and how each element flows in the document.", "p { display: block; }\nspan { display: inline; }", "p { display: block; }"),
                        build_lesson("How Does Inline-Block Work, and How Does It Differ from Inline and Block Elements?", "inline-block-usage", "Use inline-block to create flexible, controlled layout pieces.", ".tag { display: inline-block; padding: 6px 12px; }", ".tag { display: inline-block; }"),
                        build_lesson("What Are Margins and Padding, and How Do They Work?", "margins-and-padding", "Control spacing around and inside your elements to refine layout.", ".card { padding: 20px; margin: 12px 0; }", ".card { padding: 20px; margin: 12px 0; }"),
                        build_lesson("Design a Cafe Menu", "design-a-cafe-menu", "Apply CSS to build a polished, readable menu layout.", "<section class=\"menu\"><h1>Cafe Menu</h1><ul><li>Cappuccino</li></ul></section>", "<section class=\"menu\"><h1>Cafe Menu</h1></section>"),
                        build_lesson("Design a Business Card", "design-a-business-card", "Create a compact, professional card layout with spacing and hierarchy.", "<article class=\"business-card\"><h2>Jules</h2><p>Creative Developer</p></article>", "<article class=\"business-card\"><h2>Jules</h2></article>"),
                        build_lesson("CSS Specificity, the Cascade Algorithm, and Inheritance", "css-specificity-cascade-and-inheritance", "Understand why some styles win and how inheritance helps share design rules.", "p { color: #334155; }\n.card p { color: #0f172a; }", "p { color: #334155; }"),
                        build_lesson("CSS Fundamentals Review", "css-fundamentals-review", "Reconnect the most important CSS ideas before moving to more advanced layout and design topics.", "body { margin: 0; font-family: sans-serif; }\n.container { display: grid; gap: 1rem; }", "body { margin: 0; }"),
                        build_lesson("CSS Fundamentals Quiz", "css-fundamentals-quiz", "Check your grasp of selectors, spacing, and layout fundamentals.", "<form><label>What does CSS do?</label><input type=\"text\"></form>", "<form><label>Question</label></form>"),
                    ],
                },
                {
                    "title": "Styling Lists and Links",
                    "lessons": [
                        build_lesson("How Do You Space List Items Using margin or line-height?", "space-list-items", "Tune list spacing for better readability and hierarchy.", "li { margin-bottom: 0.5rem; }", "li { margin-bottom: 0.5rem; }"),
                        build_lesson("How Do the Different list-style Properties Work?", "list-style-properties", "Customize bullets, numbering, and spacing in lists.", "ul { list-style: square; }\nol { list-style-type: decimal; }", "ul { list-style: square; }"),
                        build_lesson("Why Are Default Link Styles Important for Usability on the Web?", "why-default-link-styles-matter", "Understand the browser default link states and how they help users navigate.", "a { color: #2563eb; text-decoration: underline; }", "a { color: #2563eb; }"),
                        build_lesson("How Do You Style the Different Link States?", "style-link-states", "Apply unique styles for normal, hover, active, and visited states.", "a:link { color: #2563eb; }\na:hover { color: #1d4ed8; }", "a:link { color: #2563eb; }"),
                        build_lesson("Build a Stylized To-Do List", "build-a-stylized-to-do-list", "Create a readable list interface using cleaner spacing and better link styling.", "<ul class=\"todo\"><li>Write HTML</li><li>Style CSS</li></ul>", "<ul class=\"todo\"><li>Write HTML</li></ul>"),
                    ],
                },
                {
                    "title": "Working with Backgrounds and Borders",
                    "lessons": [
                        build_lesson("How Do Background Image Size, Repeat, Position, and Attachment Work?", "background-image-size-repeat-position-attachment", "Control how background graphics behave across layouts and sections.", ".banner { background-image: url('pattern.png'); background-size: cover; background-repeat: no-repeat; }", ".banner { background-image: url('pattern.png'); }"),
                        build_lesson("What Is a Background Gradient, and How Does It Work?", "background-gradient", "Create rich backgrounds using linear or radial gradients.", ".hero { background: linear-gradient(135deg, #1d4ed8, #60a5fa); }", ".hero { background: linear-gradient(135deg, #1d4ed8, #60a5fa); }"),
                        build_lesson("What Are Some Accessibility Considerations for Backgrounds?", "accessibility-considerations-for-backgrounds", "Avoid low-contrast or decorative backgrounds that reduce readability.", ".hero { color: #ffffff; background: #0f172a; }", ".hero { color: #ffffff; }"),
                        build_lesson("What Are the Different Ways You Can Add Borders Around Images?", "borders-around-images", "Use border styles to frame and highlight visual elements.", "img { border: 2px solid #cbd5e1; border-radius: 12px; }", "img { border: 2px solid #cbd5e1; }"),
                        build_lesson("Design a Blog Post Card", "design-a-blog-post-card", "Apply backgrounds, borders, and spacing to create a elegant content card.", "<article class=\"card\"><h2>Design Notes</h2><p>Good layouts feel effortless.</p></article>", "<article class=\"card\"><h2>Design Notes</h2></article>"),
                        build_lesson("Lists, Links, CSS Background and Borders Review", "lists-links-backgrounds-and-borders-review", "Review the core visual styling ideas used across real interface design.", ".card { border: 1px solid #dfe7f5; background: #f8fafc; }", ".card { background: #f8fafc; }"),
                        build_lesson("CSS Backgrounds and Borders Quiz", "css-backgrounds-and-borders-quiz", "Check your understanding of visual styling and design details.", "<form><label>Which CSS property controls border radius?</label><input type=\"text\"></form>", "<form><label>Question</label></form>"),
                    ],
                },
                {
                    "title": "Design",
                    "lessons": [
                        build_lesson("User Interface Design Fundamentals", "user-interface-design-fundamentals", "Use design terms and visual principles to communicate clearly with users.", "<section><h2>UI Fundamentals</h2><p>Design is about clarity and intent.</p></section>", "<section><h2>UI Fundamentals</h2></section>"),
                        build_lesson("What Are Common Design Terms to Help You Communicate with Designers?", "design-terms", "Learn the vocabulary used for hierarchy, alignment, spacing, and composition.", "<p>Use hierarchy, contrast, alignment, and whitespace to shape the interface.</p>", "<p>Use hierarchy and alignment.</p>"),
                        build_lesson("How Do You Create Good Background and Foreground Contrast in Your Designs?", "contrast-in-design", "Balance readability and visual energy using contrast deliberately.", ".surface { background: #0f172a; color: #f8fafc; }", ".surface { background: #0f172a; color: #f8fafc; }"),
                        build_lesson("What Is the Importance of Good Visual Hierarchy in Design?", "visual-hierarchy", "Guide user attention using size, weight, and placement.", "h1 { font-size: 2.5rem; }\nh2 { font-size: 1.5rem; }", "h1 { font-size: 2.5rem; }"),
                        build_lesson("How Does Scale Work in Design?", "scale-in-design", "Use proportional differences in size to create a meaningful visual rhythm.", "h1 { font-size: 3rem; }\np { font-size: 1rem; }", "h1 { font-size: 3rem; }"),
                        build_lesson("How Does Alignment Work in Design?", "alignment-in-design", "Keep layouts coherent by aligning content and structure intentionally.", ".row { display: flex; justify-content: space-between; }", ".row { display: flex; }"),
                        build_lesson("What Is the Importance of Whitespace in Design?", "whitespace-in-design", "Whitespace creates breathing room and can improve the overall experience.", ".card { padding: 2rem; }", ".card { padding: 2rem; }"),
                        build_lesson("What Are Best Practices for Working with Images in Your Designs?", "images-in-design", "Use resolution, cropping, and alt text intentionally for quality and accessibility.", "<img src=\"photo.jpg\" alt=\"Open laptop on a desk\">", "<img src=\"photo.jpg\" alt=\"Open laptop\">"),
                        build_lesson("What Is Progressive Enhancement?", "what-is-progressive-enhancement", "Build a usable base and add enhancements without breaking the core experience.", "<p>Progressive enhancement starts with strong HTML and adds CSS and JavaScript safely.</p>", "<p>Progressive enhancement adds features safely.</p>"),
                        build_lesson("User-Centered Design", "user-centered-design", "Focus on the user's goals, tasks, and mental model when shaping interfaces.", "<p>User-centered design keeps the user journey obvious and easy.</p>", "<p>User-centered design matters.</p>"),
                        build_lesson("Common Design Tools", "common-design-tools", "Get comfortable using design tools to visualize, test, and refine ideas.", "<p>Design tools help you prototype and evaluate user interface direction.</p>", "<p>Design tools help with prototyping.</p>"),
                        build_lesson("Design Fundamentals Review", "design-fundamentals-review", "Review the main design principles that support readable and effective interfaces.", "<section><h2>Design Review</h2><p>Contrast, alignment, and hierarchy matter.</p></section>", "<section><h2>Design Review</h2></section>"),
                        build_lesson("Design Fundamentals Quiz", "design-fundamentals-quiz", "Check how well you understand key interface design principles.", "<form><label>What is whitespace used for?</label><input type=\"text\"></form>", "<form><label>Question</label></form>"),
                    ],
                },
                {
                    "title": "Absolute and Relative Units",
                    "lessons": [
                        build_lesson("Absolute and Relative Units Fundamentals", "absolute-and-relative-units-fundamentals", "Use pixels, ems, rems, percentages, and viewport units appropriately.", ".card { width: 50%; padding: 1rem; font-size: 1.2rem; }", ".card { width: 50%; }"),
                    ],
                },
                {
                    "title": "Pseudo Classes and Elements",
                    "lessons": [
                        build_lesson("Pseudo Classes and Elements Basics", "pseudo-classes-and-elements-basics", "Style states and generated content using CSS selectors beyond simple classes.", "a:hover { color: #1d4ed8; }\np::first-letter { font-weight: bold; }", "a:hover { color: #1d4ed8; }"),
                    ],
                },
                {
                    "title": "Colors",
                    "lessons": [
                        build_lesson("Color Theory Basics", "color-theory-basics", "Understand hue, saturation, and contrast to build a cohesive visual identity.", ".theme { color: #2563eb; background: #eff6ff; }", ".theme { color: #2563eb; }"),
                    ],
                },
                {
                    "title": "Styling Forms",
                    "lessons": [
                        build_lesson("Styling Inputs and Buttons", "styling-inputs-and-buttons", "Give forms a more polished and intentional visual treatment.", "input { border: 1px solid #cbd5e1; border-radius: 8px; padding: 0.75rem; }\nbutton { background: #2563eb; color: white; }", "input { border: 1px solid #cbd5e1; }"),
                    ],
                },
                {
                    "title": "The Box Model",
                    "lessons": [
                        build_lesson("The Box Model Overview", "box-model-overview", "Understand the content, padding, border, and margin layers of each element.", ".box { padding: 12px; border: 1px solid #dbeafe; margin: 16px; }", ".box { padding: 12px; }"),
                    ],
                },
                {
                    "title": "Flexbox",
                    "lessons": [
                        build_lesson("Build a Page of Playing Cards", "build-a-page-of-playing-cards", "Use flexbox to create balanced, responsive cards with aligned content.", "<section class=\"cards\"><article>Card 1</article><article>Card 2</article></section>", "<section class=\"cards\"><article>Card 1</article></section>"),
                    ],
                },
                {
                    "title": "Typography",
                    "lessons": [
                        build_lesson("Typography Fundamentals", "typography-fundamentals", "Use type scales, spacing, and contrast to improve readability.", "h1 { font-size: 2.5rem; }\np { line-height: 1.6; }", "h1 { font-size: 2.5rem; }"),
                    ],
                },
                {
                    "title": "Accessibility",
                    "lessons": [
                        build_lesson("Accessibility in CSS", "accessibility-in-css", "Make sure interactive elements and visual choices remain easy to understand and navigate.", ".button { background: #2563eb; color: white; }\n.button:focus { outline: 3px solid #93c5fd; }", ".button { background: #2563eb; }"),
                    ],
                },
                {
                    "title": "Positioning",
                    "lessons": [
                        build_lesson("CSS Positioning Basics", "css-positioning-basics", "Use static, relative, absolute, and fixed positioning with intention.", ".badge { position: absolute; top: 0; right: 0; }", ".badge { position: absolute; }"),
                    ],
                },
                {
                    "title": "Attribute Selectors",
                    "lessons": [
                        build_lesson("Attribute Selectors Fundamentals", "attribute-selectors-fundamentals", "Target elements by attribute value to build flexible UI patterns.", "input[type=\"email\"] { border-color: #2563eb; }", "input[type=\"email\"] { border-color: #2563eb; }"),
                    ],
                },
                {
                    "title": "Responsive Design",
                    "lessons": [
                        build_lesson("Build a Technical Documentation Page", "build-a-technical-documentation-page", "Use responsive layout patterns to create documentation pages that scale across devices.", "<main><nav>Docs</nav><article><h1>Getting Started</h1></article></main>", "<main><nav>Docs</nav></main>"),
                    ],
                },
                {
                    "title": "Variables",
                    "lessons": [
                        build_lesson("CSS Variables Fundamentals", "css-variables-fundamentals", "Store reusable colors, spacing values, and other design tokens in variables.", ":root { --brand: #2563eb; --space: 1rem; }\n.card { color: var(--brand); padding: var(--space); }", ":root { --brand: #2563eb; }"),
                    ],
                },
                {
                    "title": "Grid",
                    "lessons": [
                        build_lesson("Build a Product Landing Page", "build-a-product-landing-page", "Use grid to create structured product landing pages with interesting layouts.", "<section class=\"grid\"><article>Feature</article><article>Feature</article></section>", "<section class=\"grid\"><article>Feature</article></section>"),
                    ],
                },
                {
                    "title": "Animations",
                    "lessons": [
                        build_lesson("Animation Basics", "animation-basics", "Add motion carefully to improve the feeling of interaction and progress.", ".button { transition: transform 0.2s ease; }\n.button:hover { transform: translateY(-2px); }", ".button { transition: transform 0.2s ease; }"),
                    ],
                },
                {
                    "title": "CSS Review",
                    "lessons": [
                        build_lesson("CSS Review", "css-review", "Bring together the core CSS ideas of layout, styling, responsivity, and visual design.", "<main class=\"review\"><h1>CSS Review</h1><p>Layout, color, and spacing matter.</p></main>", "<main class=\"review\"><h1>CSS Review</h1></main>"),
                    ],
                },
            ],
        }
    ]

    for course_data in catalog:
        course = Course.query.filter_by(slug=course_data["slug"]).first()
        if course is None:
            course = Course(
                title=course_data["title"],
                slug=course_data["slug"],
                description=course_data["description"],
                category="Web Development",
                difficulty="Beginner",
                duration="6 weeks",
                instructor="HiveryTech Team",
            )
            db.session.add(course)
            db.session.flush()

        for module_index, module_data in enumerate(course_data["modules"], 1):
            module = Module.query.filter_by(course_id=course.id, title=module_data["title"]).first()
            is_existing_module = module is not None
            if module is None:
                module = Module(course=course, title=module_data["title"], position=module_index)
                db.session.add(module)
                db.session.flush()

            starter_slugs = {
                "html-from-scratch-your-first-webpage",
                "html-elements-opening-and-closing-tags",
                "html-headings-page-outline",
                "html-paragraphs-and-text-emphasis",
                "html-links-href",
                "html-images-and-alt-text",
                "html-lists-ul-ol-li",
                "html-semantic-page-structure",
            }
            has_missing_starter_lessons = (
                module_data["title"] == "Basic HTML"
                and any(
                    not Lesson.query.filter_by(module_id=module.id, slug=slug).first()
                    for slug in starter_slugs
                )
            )
            if is_existing_module and has_missing_starter_lessons:
                Lesson.query.filter_by(module_id=module.id).update(
                    {Lesson.position: Lesson.position + len(starter_slugs)},
                    synchronize_session=False,
                )
                db.session.flush()
                starter_position = 0
            else:
                starter_position = None

            for lesson_index, lesson_data in enumerate(module_data["lessons"], 1):
                if Lesson.query.filter_by(module_id=module.id, slug=lesson_data["slug"]).first():
                    continue
                if lesson_data["slug"] in starter_slugs and starter_position is not None:
                    lesson_position = lesson_index
                else:
                    max_position = db.session.query(db.func.max(Lesson.position)).filter_by(module_id=module.id).scalar() or 0
                    lesson_position = max_position + 1
                db.session.add(
                    Lesson(
                        module=module,
                        title=lesson_data["title"],
                        slug=lesson_data["slug"],
                        body=lesson_data["body"],
                        example_code=lesson_data["example_code"],
                        code=lesson_data["code"],
                        language=lesson_data["language"],
                        position=lesson_position,
                        tests=lesson_data["tests"],
                        hints=lesson_data["hints"],
                    )
                )
            db.session.flush()

    db.session.commit()

    admin_email = os.getenv("ADMIN_EMAIL", "admin@hiverytech.local").lower()
    if not User.query.filter_by(email=admin_email).first():
        admin = User(name="HiveryTech Admin", email=admin_email, is_admin=True)
        admin.set_password(os.getenv("ADMIN_PASSWORD", "ChangeMe123!"))
        db.session.add(admin)

    db.session.commit()