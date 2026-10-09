# CodeForge

CodeForge is a practical learning platform for aspiring web developers, built by HiveryTech. It is designed to feel clear, modern, and motivating like a premium coding academy while staying easier to navigate than a large course marketplace.

## What this app includes

- Structured web development learning paths
- Responsive HTML/CSS lesson editor with live preview
- Practical project-based curriculum flow
- User dashboard and lesson progress tracking
- Beginner-friendly lessons with guided hints and examples
- A step-by-step HTML-from-scratch path covering page structure, elements, headings, paragraphs, links, images, lists, and semantic HTML
- A guided CSS course that teaches selectors, colors, units, spacing, typography, box model, interaction states, forms, Flexbox, Grid, responsiveness, variables, accessibility, positioning, and transitions
- A taught CSS path covering selectors, colors, units, spacing, typography, the box model, interaction states, forms, Flexbox, Grid, responsive layouts, variables, accessibility, positioning, and transitions
- Direct course-to-lesson start links and saved lesson progress
- Search, blog, project, and challenge pages
- SEO-friendly metadata and mobile-first layout
- Certification flow for course completion and verification

## Tech stack

- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Limiter
- SQLite by default
- HTML/CSS/JS browser-based lessons

## Local setup

1. Open the project folder.
2. Create and activate a virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Start the app:

   python app.py

5. Visit:

   http://127.0.0.1:5000

## Reset database

To recreate the local database and reload the seeded course content, run:

`python reset_db.py`

**Warning:** this drops the configured database before rebuilding it. Do not run this against a production database or any database whose data you need to keep.

## Lesson progress

Learners can preview a lesson without signing in. Sign in or create an account to save completion progress. After passing the lesson checks, choose **Complete and continue** to save progress and open the next lesson. The editor also supports Ctrl+Enter (or Cmd+Enter) to run the checks.

Each lesson keeps the worked example separate from the blank learner editor. For CSS lessons, the preview contains sample HTML and updates as the learner writes styles in the CSS editor.

New curriculum lessons are added automatically when the app starts. This update is additive and does not require deleting the database or existing learner progress.

## Render deployment

This project is ready to launch on Render with a Python web service.

### Recommended Render configuration

- Web Service type: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn "app:create_app()"`
- Add environment variables:
  - `SECRET_KEY`
  - `FLASK_DEBUG=0`
  - `DATABASE_URL` for production database use
- Optional: connect a PostgreSQL database and keep SQLite only for local dev

### Example Render file

A deployment file is included at `render.yaml` for a simple Render setup.

## Project structure

- `app/` — core Flask app, models, routes, templates, and static assets
- `app/seed.py` — seeded curriculum and lesson data
- `app/templates/` — HTML pages for the platform
- `app/static/` — CSS, JS, and browser assets
- `tests/` — project test folder for future coverage
- `render.yaml` — Render deployment blueprint

## Recommended use

This project is designed to feel like a modern coding academy for beginners and self-taught developers. The learning flow is intentionally simple and realistic: learn a concept, study an example, solve a task, check your work, and continue to the next lesson.

## Production notes

- Use a real secret key in production.
- Set `DATABASE_URL` for a production database when deploying.
- Set a strong `ADMIN_PASSWORD` before first deployment; never rely on the local development default.
- Run behind HTTPS and use a reverse proxy if needed.
- The app is created to be easy to extend with more courses, modules, and projects over time.
