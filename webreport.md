# CodeForge Web Report

## Product overview

CodeForge is a Flask-based beginner learning website. The active course begins with typing and reading HTML, proceeds through HTML structure and common elements, then teaches CSS and responsive design before a complete page project. The unrelated computer-literacy material from older curriculum data is hidden from the active path without deleting stored progress records.

## Learning experience

- **Zero-assumptions HTML starting point:** explains HTML tags/elements and teaches typing angle brackets, closing slashes, attribute quotes, indentation, and how to debug common typing errors.
- **HTML from scratch:** introduces document structure, headings and paragraphs, attributes, links, images and alt text, lists, semantic landmarks, forms, and data tables.
- **CSS from scratch:** explains CSS rules and selectors, color and contrast, values and units, the box model, spacing, typography, normal flow/display, Flexbox, Grid, responsive design, keyboard focus, and reduced motion.
- **Guided practice:** lesson explanations, worked examples, starter code, lesson checks, sequential hints, and a live HTML/CSS preview support the learn → observe → try → check cycle.
- **Project practice:** the existing curriculum includes projects, challenges, articles, and review material.
- **No completion throttle:** learners may open and revisit lessons freely. Lesson checks guide progress but do not restrict access to later lesson pages.

## Progress, drafts, and certificates

- Lesson completion is recorded once per user and lesson; repeated completion does not grant duplicate XP.
- The course page selects the next unfinished lesson for a learner, and completion routes to the following lesson.
- Editor drafts continue saving in browser local storage. Authenticated users also autosave drafts to their account, so work can be restored on another device or browser after sign-in.
- Draft saving is separate from lesson completion. Completing a lesson does not clear the code draft; the editor's Reset button is the explicit action that clears the local draft.
- Certificate claims require every lesson in the course to be complete. Existing certificates are reused rather than duplicated, and certificate IDs have a public verification page.
- Lesson success triggers confetti, with an in-page fallback if the optional confetti CDN is unavailable.
- A stored, server-graded final exam covers core HTML/CSS concepts. Learners need at least 70% after completing lessons before the certificate claim is allowed; retries are permitted.

## SEO and discoverability

- Page-specific title and description metadata, canonical URLs, Open Graph metadata, and social card descriptions are rendered from templates.
- Course pages include Schema.org Course JSON-LD.
- `/robots.txt` provides crawler directions and the sitemap URL; `/sitemap.xml` lists published courses, lessons, and articles.
- Account/admin and certificate verification pages are marked `noindex, nofollow`; public learning content remains indexable.
- SEO work helps crawlers understand and find content but cannot guarantee indexing or rankings. After deployment, verify ownership and sitemap in Google Search Console and inspect representative URLs.
- Guidance reviewed: [MDN: What is CSS?](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/What_is_CSS) and [Google Search Central: SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide). MDN recommends learning rule syntax and experimenting in a live preview; Google emphasizes useful content, clear page titles/descriptions, crawlable links, and sitemaps (not meta-keyword stuffing).

## Technology

- **Server:** Python 3, Flask, Flask-SQLAlchemy, SQLAlchemy, Flask-Login, Flask-WTF CSRF protection, Flask-Migrate.
- **Data:** SQLite by default; PostgreSQL driver included for deployment configuration.
- **Frontend:** Jinja templates, HTML, responsive CSS, browser JavaScript, local storage, iframe-based live preview, optional canvas-confetti and Pyodide CDN scripts.
- **PWA:** root-scoped service worker, installable web manifest and SVG icon, install prompt, offline shell, and network-first caching of previously visited public course and lesson pages. Authenticated lesson pages are marked private/no-store and are not cached.
- **Deployment:** Gunicorn and Render configuration files are present.
- **Progress data:** users, courses, modules, lessons, lesson completions, account-backed lesson drafts, enrollments, certificates, challenges, projects, and articles.

## Main project areas

- `app/__init__.py` — Flask setup, extensions, database creation, and additive curriculum seeding.
- `app/models.py` — relational data models, including lesson progress, drafts, and certificates.
- `app/routes.py` — course, lesson, draft, completion, certificate, verification, search, and SEO endpoints.
- `app/beginner_curriculum.py` — beginner HTML typing, HTML structure, CSS, and project lessons.
- `app/seed.py` — course catalog and additive seed/update behavior; does not require dropping the database.
- `app/templates/` — Jinja pages and lesson editor.
- `app/static/css/app.css` — responsive layout and visual styles, including confetti fallback animation.
- `app/static/js/app.js` — editor persistence, live preview, lesson checks, progression, and celebration.
- `tests/test_learning_flow.py` — integration tests for lessons, drafts, progress, certificates, and SEO routes.

## Validation status

An in-memory automated integration suite is provided for the core learning flows. It covers:

1. HTML-first course and blank HTML/CSS editor rendering.
2. Idempotent lesson completion and XP/progress preservation.
3. Account draft autosave.
4. Certificate denial before completion and before passing the final exam, then claim and public verification.
5. `robots.txt`, `sitemap.xml`, manifest, and root-scoped service worker availability.

Browser rendering and SEO indexing are environment/deployment checks; indexing itself can only be observed after publishing the website and waiting for crawlers.

## Important operational note

The new lessons and account draft table are added using the app's existing `db.create_all()`/additive seeding approach. Do **not** run `reset_db.py` on a database with learner data; it drops the configured database. Set a production `SECRET_KEY`, use a persistent production database, deploy over HTTPS, and keep backups.
