import json
import os

from . import db
from .models import Course, Lesson, LessonProgress, Module, User


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
                                        "CSS from Scratch: Style Your First Page",
                                        "css-from-scratch-first-styles",
                                        "<p><strong>What CSS does:</strong> HTML describes what content is; CSS describes how it looks. A CSS rule has a selector (what to style) and declarations (which visual changes to make).</p><p><strong>Read this rule:</strong> in <code>p { color: navy; }</code>, <code>p</code> selects every paragraph and <code>color: navy</code> changes its text color. The braces hold the declarations, and each declaration ends with a semicolon.</p><p><strong>Your task:</strong> select the page body and set a readable font. Then give the heading a color. Use the styles.css editor tab.</p>",
                                        "body {\n  font-family: Arial, sans-serif;\n}\n\nh1 {\n  color: #2563eb;\n}",
                                        "body {\n  font-family: Arial, sans-serif;\n}\n",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('body')", "message": "Add a CSS rule for body."},
                                            {"test": "code.includes('font-family')", "message": "Set a font-family for readable text."},
                                            {"test": "code.includes('h1') && code.includes('color')", "message": "Add a color declaration for the h1 heading."}
                                        ],
                                        hints=["Write body followed by curly braces.", "Inside the body rule, add font-family: Arial, sans-serif;", "Add a second rule for h1 and set its color."]
                                    ),
                                    build_lesson(
                                        "CSS Selectors: Choose What to Style",
                                        "css-selectors-elements-classes-ids",
                                        "<p><strong>Understand it:</strong> a selector chooses which HTML elements receive a rule. A type selector like <code>p</code> selects all paragraphs. A class selector starts with a dot, like <code>.card</code>, and can be reused. An ID selector starts with <code>#</code> and is intended for one unique element.</p><p>In <code>&lt;article class=\"card\"&gt;</code>, the matching selector is <code>.card</code>. Class names do not include the dot in HTML; the dot is only CSS selector syntax.</p><p><strong>Your task:</strong> style every paragraph, then create a reusable .card rule.</p>",
                                        "p {\n  color: #334155;\n}\n\n.card {\n  background-color: #eff6ff;\n}",
                                        "p {\n  color: #334155;\n}\n",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('p') && code.includes('color')", "message": "Style paragraph elements using a p selector."},
                                            {"test": "code.includes('.card')", "message": "Create a reusable class selector named .card."},
                                            {"test": "code.includes('background-color')", "message": "Give the card a background color."}
                                        ],
                                        hints=["A type selector is just the element name: p.", "Start the class selector with a dot: .card.", "Use background-color inside the .card rule."]
                                    ),
                                    build_lesson(
                                        "CSS Colors and Readable Contrast",
                                        "css-colors-and-contrast",
                                        "<p><strong>Understand it:</strong> CSS colors can use names, hexadecimal values such as <code>#1d4ed8</code>, or RGB values. Use <code>color</code> for text and <code>background-color</code> for the element's background.</p><p><strong>Accessibility tip:</strong> text needs enough contrast against its background to be readable. Avoid pale text on a pale background.</p><p><strong>Your task:</strong> give the page a light background and set the text to a dark, readable color.</p>",
                                        "body {\n  color: #1e293b;\n  background-color: #f8fafc;\n}",
                                        "body {\n  color: #1e293b;\n}",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('color:')", "message": "Set a text color."},
                                            {"test": "code.includes('background-color:')", "message": "Set a background color."}
                                        ],
                                        hints=["Use color for the text.", "Use background-color for the page surface.", "A dark text color on a light background is a readable choice."]
                                    ),
                                    build_lesson(
                                        "CSS Units: Pixels, rem, and Percentages",
                                        "css-units-pixels-rem-percentages",
                                        "<p><strong>Understand it:</strong> CSS values need units when they represent size or distance. <code>px</code> is a fixed-size unit. <code>rem</code> scales relative to the root text size, which often helps accessible typography. <code>%</code> is relative to a containing size.</p><p><strong>Your task:</strong> make the page text comfortable to read with a rem size, and limit the main content width with a percentage.</p>",
                                        "body {\n  font-size: 1rem;\n}\n\nmain {\n  width: 90%;\n}",
                                        "body {\n  font-size: 16px;\n}",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('font-size') && /font-size\\s*:[^;]*rem/.test(code)", "message": "Set font-size using rem units."},
                                            {"test": "code.includes('width') && code.includes('%')", "message": "Use a percentage width for the main content."}
                                        ],
                                        hints=["Use font-size: 1rem; on body.", "Create a main selector.", "A width such as 90% adapts to the available space."]
                                    ),
                                    build_lesson(
                                        "Spacing with Margin and Padding",
                                        "css-margin-and-padding",
                                        "<p><strong>Understand it:</strong> padding is space inside an element, between its content and border. Margin is space outside an element, separating it from neighbors. Think of padding as the cushion inside a box and margin as the gap around the box.</p><p><strong>Your task:</strong> add comfortable inner space to a card and room around it.</p>",
                                        ".card {\n  padding: 1.5rem;\n  margin: 1rem;\n}",
                                        ".card {\n  padding: 1rem;\n}",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('.card')", "message": "Target the card class."},
                                            {"test": "code.includes('padding:')", "message": "Add inner spacing with padding."},
                                            {"test": "code.includes('margin:')", "message": "Add outer spacing with margin."}
                                        ],
                                        hints=["Keep the .card selector.", "Padding is inside the element.", "Add margin for space outside it."]
                                    ),
                                    build_lesson(
                                        "Borders, Width, and the Box Model",
                                        "css-borders-width-box-model",
                                        "<p><strong>Understand it:</strong> every element is a box made of content, padding, border, and margin. The <code>border</code> draws an edge around the padding and content. <code>border-radius</code> rounds its corners. Width controls the content size unless you change the box-sizing model.</p><p><strong>Your task:</strong> give a card a border, rounded corners, and a sensible width.</p>",
                                        ".card {\n  width: 100%;\n  border: 1px solid #cbd5e1;\n  border-radius: 12px;\n  box-sizing: border-box;\n}",
                                        ".card {\n  border: 1px solid #cbd5e1;\n}",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('border:')", "message": "Add a border to the card."},
                                            {"test": "code.includes('border-radius')", "message": "Round the card corners."},
                                            {"test": "code.includes('width:')", "message": "Set the card width."}
                                        ],
                                        hints=["Use the .card selector.", "The border shorthand can include width, style, and color.", "Add border-radius and width declarations."]
                                    ),
                                    build_lesson(
                                        "Typography: Fonts, Line Height, and Text Alignment",
                                        "css-typography-and-line-height",
                                        "<p><strong>Understand it:</strong> typography affects how easily people can read. <code>font-family</code> chooses a typeface, <code>font-size</code> controls its size, and <code>line-height</code> controls vertical space between lines. A line-height around 1.5 is a useful starting point for body text.</p><p><strong>Your task:</strong> set a sans-serif font and improve paragraph line spacing.</p>",
                                        "body {\n  font-family: Arial, sans-serif;\n}\n\np {\n  line-height: 1.5;\n}",
                                        "body {\n  font-family: Arial, sans-serif;\n}",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('font-family')", "message": "Choose a font family."},
                                            {"test": "code.includes('line-height')", "message": "Set comfortable line spacing."}
                                        ],
                                        hints=["Set font-family on body.", "Add a p rule.", "Try line-height: 1.5; for paragraphs."]
                                    ),
                                    build_lesson(
                                        "Pseudo-Classes: Style Interaction States",
                                        "css-pseudo-classes-hover-focus",
                                        "<p><strong>Understand it:</strong> a pseudo-class styles an element in a particular state. <code>:hover</code> applies while a pointer is over a link or button. <code>:focus</code> applies when it is selected using a keyboard or other input.</p><p><strong>Accessibility tip:</strong> do not remove the keyboard focus indicator unless you replace it with an equally visible one.</p><p><strong>Your task:</strong> add a hover color and a clear focus outline for links.</p>",
                                        "a:hover {\n  color: #1d4ed8;\n}\n\na:focus {\n  outline: 3px solid #93c5fd;\n}",
                                        "a:hover {\n  color: #1d4ed8;\n}",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('a:hover')", "message": "Add a hover state for links."},
                                            {"test": "code.includes('a:focus') && code.includes('outline')", "message": "Provide a visible keyboard focus style."}
                                        ],
                                        hints=["Use a:hover as a selector.", "Create a second selector: a:focus.", "Add an outline so keyboard focus remains visible."]
                                    ),
                                    build_lesson(
                                        "CSS Layout with Flexbox",
                                        "css-flexbox-first-layout",
                                        "<p><strong>Understand it:</strong> Flexbox arranges items along a row or column. Set <code>display: flex</code> on a parent container to make its direct children flex items. Use <code>gap</code> to add even space between them.</p><p><strong>Your task:</strong> place a group of cards in a row with space between cards. On narrow screens, layouts can wrap with <code>flex-wrap: wrap</code>.</p>",
                                        ".cards {\n  display: flex;\n  flex-wrap: wrap;\n  gap: 1rem;\n}",
                                        ".cards {\n  display: flex;\n}",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('.cards') && code.includes('display: flex')", "message": "Turn the cards container into a flex container."},
                                            {"test": "code.includes('gap:')", "message": "Add consistent space between flex items."},
                                            {"test": "code.includes('flex-wrap')", "message": "Allow items to wrap on smaller screens."}
                                        ],
                                        hints=["Flexbox is applied to the parent container.", "Use display: flex; on .cards.", "Add gap and flex-wrap declarations."]
                                    ),
                                    build_lesson(
                                        "Responsive CSS with Media Queries",
                                        "css-responsive-media-queries",
                                        "<p><strong>Understand it:</strong> a media query applies styles only when a condition is true, such as when the screen is narrow. This lets you adjust layouts for phones without duplicating the whole stylesheet.</p><p><strong>Read this:</strong> <code>@media (max-width: 600px)</code> means the rules inside apply when the viewport is 600 pixels wide or less.</p><p><strong>Your task:</strong> write a media query that makes the page heading smaller on narrow screens.</p>",
                                        "@media (max-width: 600px) {\n  h1 {\n    font-size: 2rem;\n  }\n}",
                                        "@media (max-width: 600px) {\n  h1 {\n    font-size: 2rem;\n  }\n}",
                                        language="css",
                                        tests=[
                                            {"test": "code.includes('@media')", "message": "Add a media query."},
                                            {"test": "code.includes('max-width')", "message": "Use a maximum-width condition for smaller screens."},
                                            {"test": "code.includes('font-size')", "message": "Adjust the heading font size inside the query."}
                                        ],
                                        hints=["Start with @media and parentheses.", "Try (max-width: 600px).", "Put an h1 font-size rule inside the braces."]
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
                        build_lesson(
                            "Style a Link Clearly",
                            "css-style-links",
                            "<p><strong>Understand it:</strong> the <code>a</code> selector styles links. The <code>text-decoration</code> property controls underline and other line decoration. Keep links visually distinguishable from ordinary text so visitors can recognize what is clickable.</p><p><strong>Your task:</strong> give links a clear blue color and keep their underline.</p>",
                            "a {\n  color: #2563eb;\n  text-decoration: underline;\n}",
                            "a {\n  color: #2563eb;\n}",
                            language="css",
                            tests=[{"test": "code.includes('a') && code.includes('color:')", "message": "Set a visible color for links."}, {"test": "code.includes('text-decoration')", "message": "Set an explicit link text decoration."}],
                            hints=["Use a as the selector.", "Set its color.", "Keep links underlined with text-decoration."]
                        ),
                        build_lesson(
                            "Style Hover and Focus States",
                            "css-style-hover-focus-states",
                            "<p><strong>Understand it:</strong> pseudo-classes add styles for interaction states. <code>:hover</code> responds to a pointer; <code>:focus</code> shows which control is selected by a keyboard. Interactive elements should provide feedback for both.</p><p><strong>Your task:</strong> make hovered links change color and make focused links show an outline.</p>",
                            "a:hover { color: #1d4ed8; }\na:focus { outline: 3px solid #93c5fd; }",
                            "a:hover { color: #1d4ed8; }",
                            language="css",
                            tests=[{"test": "code.includes('a:hover')", "message": "Add a hover state."}, {"test": "code.includes('a:focus') && code.includes('outline')", "message": "Add a visible focus outline."}],
                            hints=["Start with the a:hover selector.", "Add a separate a:focus rule.", "Set an outline on the focus rule."]
                        ),
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
                        build_lesson(
                            "Add Backgrounds and Borders to a Card",
                            "css-card-backgrounds-and-borders",
                            "<p><strong>Understand it:</strong> <code>background-color</code> fills an element's background. <code>border</code> draws an edge around it, and <code>border-radius</code> rounds the corners. Keep foreground text readable against the background.</p><p><strong>Your task:</strong> give a card a pale background and a subtle border.</p>",
                            ".card {\n  background-color: #eff6ff;\n  border: 1px solid #bfdbfe;\n  border-radius: 12px;\n}",
                            ".card {\n  background-color: #eff6ff;\n}",
                            language="css",
                            tests=[{"test": "code.includes('background-color')", "message": "Set a card background."}, {"test": "code.includes('border:')", "message": "Add a border around the card."}, {"test": "code.includes('border-radius')", "message": "Round the card corners."}],
                            hints=["Target the .card class.", "Add a border declaration.", "Use border-radius for rounded corners."]
                        ),
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
                        build_lesson(
                            "The CSS Box Model: Content, Padding, Border, Margin",
                            "css-box-model-content-padding-border-margin",
                            "<p><strong>Understand it:</strong> each element is a rectangular box. From inside to outside, it has content, padding, border, and margin. Padding adds room inside the border; margin adds room outside it. The <code>box-sizing: border-box</code> rule makes declared width include padding and border, which is often easier to reason about.</p><p><strong>Your task:</strong> make the card's total width predictable and add both inner and outer spacing.</p>",
                            ".card {\n  box-sizing: border-box;\n  width: 100%;\n  padding: 1rem;\n  margin: 1rem 0;\n  border: 1px solid #cbd5e1;\n}",
                            ".card {\n  padding: 1rem;\n}",
                            language="css",
                            tests=[{"test": "code.includes('padding:')", "message": "Add space inside the box."}, {"test": "code.includes('margin:')", "message": "Add space outside the box."}, {"test": "code.includes('border:')", "message": "Include the border layer."}, {"test": "code.includes('box-sizing')", "message": "Set box-sizing to make width easier to manage."}],
                            hints=["Padding is internal space.", "Margin is external space.", "Add box-sizing: border-box; to the card rule."]
                        ),
                        build_lesson("The Box Model Overview", "box-model-overview", "Understand the content, padding, border, and margin layers of each element.", ".box { padding: 12px; border: 1px solid #dbeafe; margin: 16px; }", ".box { padding: 12px; }"),
                    ],
                },
                {
                    "title": "Flexbox",
                    "lessons": [
                        build_lesson(
                            "Flexbox: Align Items in a Row",
                            "css-flexbox-align-items",
                            "<p><strong>Understand it:</strong> Flexbox is a layout system for arranging a group of items. Put <code>display: flex</code> on the parent. <code>justify-content</code> distributes items along the main axis; <code>align-items</code> aligns them across the other axis. A <code>gap</code> creates consistent spacing.</p><p><strong>Your task:</strong> arrange the card items in a row, center them vertically, and create a gap.</p>",
                            ".cards {\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  gap: 1rem;\n}",
                            ".cards {\n  display: flex;\n}",
                            language="css",
                            tests=[{"test": "code.includes('display: flex')", "message": "Make .cards a flex container."}, {"test": "code.includes('justify-content')", "message": "Set how items are distributed along the row."}, {"test": "code.includes('align-items')", "message": "Align items across the row."}, {"test": "code.includes('gap:')", "message": "Add consistent spacing between items."}],
                            hints=["Flexbox goes on the parent container.", "Use justify-content and align-items for alignment.", "Use gap to space the cards."]
                        ),
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
                        build_lesson(
                            "CSS Grid: Build Simple Columns",
                            "css-grid-simple-columns",
                            "<p><strong>Understand it:</strong> CSS Grid lays out content in rows and columns. Set <code>display: grid</code> on a parent, then describe columns with <code>grid-template-columns</code>. <code>repeat(2, 1fr)</code> means two equal-width columns.</p><p><strong>Your task:</strong> turn the feature container into a two-column grid with a gap between cards.</p>",
                            ".features {\n  display: grid;\n  grid-template-columns: repeat(2, 1fr);\n  gap: 1rem;\n}",
                            ".features {\n  display: grid;\n}",
                            language="css",
                            tests=[{"test": "code.includes('display: grid')", "message": "Turn the container into a grid."}, {"test": "code.includes('grid-template-columns')", "message": "Define the grid columns."}, {"test": "code.includes('gap:')", "message": "Add space between grid items."}],
                            hints=["Add display: grid; to .features.", "Use repeat(2, 1fr) for two equal columns.", "Set a gap between the cards."]
                        ),
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
        modules_by_title = {module["title"]: module for module in course_data["modules"]}
        html_module = modules_by_title.get("Basic HTML")
        css_module = modules_by_title.get("Basic CSS")
        if html_module and css_module:
            misplaced_css_lessons = [
                lesson for lesson in html_module["lessons"]
                if lesson.get("language") == "css"
            ]
            html_module["lessons"] = [
                lesson for lesson in html_module["lessons"]
                if lesson.get("language") != "css"
            ]
            css_module["lessons"] = misplaced_css_lessons + css_module["lessons"]

        css_extensions = {
            "Absolute and Relative Units": [
                build_lesson("Choose CSS Units for Flexible Layouts", "css-practice-units", "<p><strong>Understand it:</strong> <code>px</code> is fixed, <code>rem</code> scales with the root font size, and percentages adapt to a parent. Relative units can make layouts more adaptable.</p><p><strong>Your task:</strong> use rem for text and a percentage for a card width.</p>", "body { font-size: 1rem; }\n.card { width: 90%; }", "", language="css", tests=[{"test": "code.includes('font-size') && /font-size\\s*:[^;]*rem/.test(code)", "message": "Use rem for the font size."}, {"test": "code.includes('.card') && code.includes('width') && code.includes('%')", "message": "Give the card a flexible percentage width."}], hints=["Set body font-size using rem.", "Create a .card rule.", "Try width: 90%;."]),
            ],
            "Pseudo Classes and Elements": [
                build_lesson("Style Hover, Focus, and First Letters", "css-practice-pseudo-classes", "<p><strong>Understand it:</strong> pseudo-classes such as <code>:hover</code> and <code>:focus</code> style an element's state. Pseudo-elements such as <code>::first-letter</code> style part of an element. Keep keyboard focus visible.</p><p><strong>Your task:</strong> add hover, focus, and first-letter rules.</p>", "button:hover { color: #1d4ed8; }\nbutton:focus { outline: 3px solid #93c5fd; }\np::first-letter { font-weight: bold; }", "", language="css", tests=[{"test": "code.includes(':hover')", "message": "Add a hover state."}, {"test": "code.includes(':focus') && code.includes('outline')", "message": "Keep keyboard focus visible."}, {"test": "code.includes('::first-letter')", "message": "Style the first letter with a pseudo-element."}], hints=["Use :hover for pointer interaction.", "Use :focus and outline for keyboard users.", "Pseudo-elements use two colons."]),
            ],
            "Colors": [
                build_lesson("Create a Readable Color Theme", "css-practice-colors", "<p><strong>Understand it:</strong> CSS supports named, hexadecimal, RGB, and HSL colors. <code>color</code> sets foreground text; <code>background-color</code> sets the surface. Strong contrast improves readability.</p><p><strong>Your task:</strong> give the page readable text and background colors, then set a distinct link color.</p>", "body { color: #172033; background-color: #f8fafc; }\na { color: #1d4ed8; }", "", language="css", tests=[{"test": "code.includes('color:')", "message": "Set a text color."}, {"test": "code.includes('background-color:')", "message": "Set a page background color."}, {"test": "code.includes('a') && code.includes('color')", "message": "Give links a distinct color."}], hints=["Use color for text.", "Use background-color for the surface.", "Add a separate a rule for links."]),
            ],
            "Styling Forms": [
                build_lesson("Style Form Fields and Buttons", "css-practice-style-forms", "<p><strong>Understand it:</strong> comfortable padding, clear borders, and visible focus styles help make forms easier to use. Do not remove the keyboard focus indicator without replacing it.</p><p><strong>Your task:</strong> style an input and button and add a visible focus outline.</p>", "input { padding: 0.75rem; border: 1px solid #94a3b8; }\ninput:focus { outline: 3px solid #93c5fd; }\nbutton { background-color: #2563eb; color: white; }", "", language="css", tests=[{"test": "code.includes('input') && code.includes('border')", "message": "Give input fields a visible border."}, {"test": "code.includes('button') && code.includes('background-color')", "message": "Style the button background."}, {"test": "code.includes(':focus') && code.includes('outline')", "message": "Provide visible keyboard focus."}], hints=["Start with an input selector.", "Add a button rule.", "Include a focus rule with an outline."]),
            ],
            "Typography": [
                build_lesson("Create a Readable Type Scale", "css-practice-typography", "<p><strong>Understand it:</strong> typography shapes readability. Use <code>font-family</code> to choose a typeface, <code>font-size</code> for hierarchy, and <code>line-height</code> for space between lines.</p><p><strong>Your task:</strong> choose a sans-serif font, enlarge the main heading, and improve paragraph line spacing.</p>", "body { font-family: Arial, sans-serif; }\nh1 { font-size: 2.5rem; }\np { line-height: 1.6; }", "", language="css", tests=[{"test": "code.includes('font-family')", "message": "Choose a font family."}, {"test": "code.includes('h1') && code.includes('font-size')", "message": "Set a heading size."}, {"test": "code.includes('line-height')", "message": "Set comfortable line spacing."}], hints=["Set font-family on body.", "Give h1 a font-size.", "Use line-height on paragraphs."]),
            ],
            "Accessibility": [
                build_lesson("Accessible CSS: Focus, Contrast, and Motion", "css-practice-accessibility", "<p><strong>Understand it:</strong> CSS affects whether an interface is usable. Keep text contrast strong, provide a clear keyboard focus ring, and respect reduced-motion preferences.</p><p><strong>Your task:</strong> add a visible focus indicator and disable optional transitions when reduced motion is requested.</p>", "button:focus-visible { outline: 3px solid #2563eb; }\n@media (prefers-reduced-motion: reduce) {\n  .button { transition: none; }\n}", "", language="css", tests=[{"test": "code.includes(':focus') && code.includes('outline')", "message": "Provide visible keyboard focus."}, {"test": "code.includes('prefers-reduced-motion')", "message": "Respect the reduced-motion preference."}], hints=["Use :focus-visible for keyboard focus.", "Set a clear outline.", "Use a prefers-reduced-motion media query."]),
            ],
            "Positioning": [
                build_lesson("Position a Badge on a Card", "css-practice-positioning", "<p><strong>Understand it:</strong> normal flow places elements in sequence. A relatively positioned parent becomes the reference point for an absolutely positioned child.</p><p><strong>Your task:</strong> make the card the positioning context, then place its badge in the top-right corner.</p>", ".card { position: relative; }\n.badge { position: absolute; top: 0; right: 0; }", "", language="css", tests=[{"test": "code.includes('.card') && code.includes('position: relative')", "message": "Make the card a positioning context."}, {"test": "code.includes('.badge') && code.includes('position: absolute')", "message": "Position the badge absolutely."}, {"test": "code.includes('top:') && code.includes('right:')", "message": "Place it at the top right."}], hints=["Set .card to position: relative.", "Set .badge to position: absolute.", "Use top: 0 and right: 0."]),
            ],
            "Attribute Selectors": [
                build_lesson("Select Form Fields by Attribute", "css-practice-attribute-selectors", "<p><strong>Understand it:</strong> attribute selectors match elements by an HTML attribute. For example, <code>input[type=\"email\"]</code> selects email fields without requiring a special class.</p><p><strong>Your task:</strong> set a border color for email inputs.</p>", "input[type=\"email\"] { border-color: #2563eb; }", "", language="css", tests=[{"test": "code.includes('input[type=')", "message": "Use an attribute selector for email fields."}, {"test": "code.includes('border-color')", "message": "Set the field border color."}], hints=["Start with input[type=\"email\"].", "Add a declaration inside braces.", "Use border-color to change the border color."]),
            ],
            "Responsive Design": [
                build_lesson("Make a Card Layout Responsive", "css-practice-responsive-layout", "<p><strong>Understand it:</strong> responsive design lets a layout adapt to available space. Media queries apply CSS only when a condition is true. A mobile-first layout can start with one column and add columns on wider screens.</p><p><strong>Your task:</strong> create one column by default and two columns at 700 pixels or wider.</p>", ".cards { display: grid; grid-template-columns: 1fr; gap: 1rem; }\n@media (min-width: 700px) { .cards { grid-template-columns: repeat(2, 1fr); } }", "", language="css", tests=[{"test": "code.includes('display: grid')", "message": "Use grid for the cards."}, {"test": "code.includes('@media') && code.includes('min-width')", "message": "Add a wider-screen media query."}, {"test": "code.includes('grid-template-columns')", "message": "Define responsive columns."}], hints=["Start with one column.", "Add @media (min-width: 700px).", "Inside the query, use two equal columns."]),
            ],
            "Variables": [
                build_lesson("Reuse Values with CSS Custom Properties", "css-practice-custom-properties", "<p><strong>Understand it:</strong> custom properties store reusable values. Define a name beginning with <code>--</code> (often on <code>:root</code>) and retrieve it using <code>var(--name)</code>.</p><p><strong>Your task:</strong> define a color and spacing token, then reuse both in a card rule.</p>", ":root { --brand: #2563eb; --space: 1rem; }\n.card { color: var(--brand); padding: var(--space); }", "", language="css", tests=[{"test": "code.includes('--brand:')", "message": "Define a brand custom property."}, {"test": "code.includes('--space:')", "message": "Define a spacing custom property."}, {"test": "code.includes('var(--brand)') && code.includes('var(--space)')", "message": "Reuse the tokens with var()."}], hints=["Define variables inside :root.", "Names start with two hyphens.", "Read them with var(--brand) and var(--space)."]),
            ],
            "Animations": [
                build_lesson("Add a Small, Respectful Transition", "css-practice-transitions", "<p><strong>Understand it:</strong> transitions smooth CSS changes between states. Choose the property and duration, then keep motion subtle. Respect people who request reduced motion.</p><p><strong>Your task:</strong> add a short button hover transition and disable it for reduced-motion users.</p>", ".button { transition: transform 180ms ease; }\n.button:hover { transform: translateY(-2px); }\n@media (prefers-reduced-motion: reduce) { .button { transition: none; } }", "", language="css", tests=[{"test": "code.includes('transition:')", "message": "Add a transition."}, {"test": "code.includes(':hover')", "message": "Create an interaction state."}, {"test": "code.includes('prefers-reduced-motion')", "message": "Respect reduced motion."}], hints=["Add transition to .button.", "Change a property on hover.", "Turn the transition off in a reduced-motion query."]),
            ],
        }
        for module_title, lessons in css_extensions.items():
            target_module = modules_by_title.get(module_title)
            if target_module:
                target_module["lessons"] = lessons + target_module["lessons"]

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
            css_starter_slugs = {
                "css-from-scratch-first-styles",
                "css-selectors-elements-classes-ids",
                "css-colors-and-contrast",
                "css-units-pixels-rem-percentages",
                "css-margin-and-padding",
                "css-borders-width-box-model",
                "css-typography-and-line-height",
                "css-pseudo-classes-hover-focus",
                "css-flexbox-first-layout",
                "css-responsive-media-queries",
                "css-style-links",
                "css-style-hover-focus-states",
                "css-card-backgrounds-and-borders",
                "css-box-model-content-padding-border-margin",
                "css-flexbox-align-items",
                "css-grid-simple-columns",
            }
            module_intro_slugs = {
                "Basic HTML": starter_slugs,
                "Basic CSS": {slug for slug in css_starter_slugs if slug not in {
                    "css-style-links", "css-style-hover-focus-states",
                    "css-card-backgrounds-and-borders",
                    "css-box-model-content-padding-border-margin",
                    "css-flexbox-align-items", "css-grid-simple-columns"
                }},
                "Styling Lists and Links": {"css-style-links", "css-style-hover-focus-states"},
                "Working with Backgrounds and Borders": {"css-card-backgrounds-and-borders"},
                "The Box Model": {"css-box-model-content-padding-border-margin"},
                "Flexbox": {"css-flexbox-align-items"},
                "Grid": {"css-grid-simple-columns"},
            }
            introductory_slugs = module_intro_slugs.get(module_data["title"], set())
            has_missing_starter_lessons = bool(introductory_slugs) and any(
                not Lesson.query.filter_by(module_id=module.id, slug=slug).first()
                for slug in introductory_slugs
            )
            if is_existing_module and has_missing_starter_lessons:
                Lesson.query.filter_by(module_id=module.id).update(
                    {Lesson.position: Lesson.position + len(introductory_slugs)},
                    synchronize_session=False,
                )
                db.session.flush()
                starter_position = 0
            else:
                starter_position = None

            for lesson_index, lesson_data in enumerate(module_data["lessons"], 1):
                if Lesson.query.filter_by(module_id=module.id, slug=lesson_data["slug"]).first():
                    continue
                if lesson_data["slug"] in introductory_slugs and starter_position is not None:
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

        html_module = Module.query.filter_by(course_id=course.id, title="Basic HTML").first()
        css_module = Module.query.filter_by(course_id=course.id, title="Basic CSS").first()
        if html_module and css_module:
            misplaced_lessons = Lesson.query.filter_by(module_id=html_module.id, language="css").all()
            for old_lesson in misplaced_lessons:
                existing_css_lesson = Lesson.query.filter_by(
                    module_id=css_module.id,
                    slug=old_lesson.slug,
                ).first()
                if existing_css_lesson:
                    old_progress = LessonProgress.query.filter_by(lesson_id=old_lesson.id).all()
                    for progress in old_progress:
                        already_completed = LessonProgress.query.filter_by(
                            user_id=progress.user_id,
                            lesson_id=existing_css_lesson.id,
                        ).first()
                        if already_completed:
                            db.session.delete(progress)
                        else:
                            progress.lesson_id = existing_css_lesson.id
                    db.session.delete(old_lesson)
                else:
                    last_position = db.session.query(db.func.max(Lesson.position)).filter_by(module_id=css_module.id).scalar() or 0
                    old_lesson.module_id = css_module.id
                    old_lesson.position = last_position + 1
            db.session.flush()

    db.session.commit()

    admin_email = os.getenv("ADMIN_EMAIL", "admin@hiverytech.local").lower()
    if not User.query.filter_by(email=admin_email).first():
        admin = User(name="HiveryTech Admin", email=admin_email, is_admin=True)
        admin.set_password(os.getenv("ADMIN_PASSWORD", "ChangeMe123!"))
        db.session.add(admin)

    db.session.commit()