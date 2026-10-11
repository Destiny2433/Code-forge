from datetime import datetime
import json
import uuid
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, abort, current_app, make_response, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from . import db
from .models import User, Course, Lesson, LessonProgress, LessonDraft, ExamAttempt, Enrollment, Challenge, Project, Certificate, Article

bp = Blueprint("main", __name__)

COURSE_EXAM = [
    {"question": "What does HTML mainly describe?", "choices": ["The structure and meaning of page content", "The color of every button", "The server's password"], "answer": 0},
    {"question": "Which tag creates the main page heading?", "choices": ["<p>", "<h1>", "<head>"], "answer": 1},
    {"question": "Where does visible page content belong?", "choices": ["<body>", "<title>", "<meta>"], "answer": 0},
    {"question": "Which attribute gives a link its destination?", "choices": ["src", "alt", "href"], "answer": 2},
    {"question": "Why should a meaningful image have alt text?", "choices": ["It describes useful image content to people who cannot see it", "It makes the image download faster", "It changes the image color"], "answer": 0},
    {"question": "Which list is best when order matters?", "choices": ["<ul>", "<ol>", "<div>"], "answer": 1},
    {"question": "What does CSS primarily control?", "choices": ["The presentation and layout of content", "The meaning of every paragraph", "The browser's internet connection"], "answer": 0},
    {"question": "In CSS, what does .card select?", "choices": ["An element with class=\"card\"", "An element with id=\"card\"", "Every card image file"], "answer": 0},
    {"question": "Which property adds space inside an element's border?", "choices": ["margin", "padding", "outline"], "answer": 1},
    {"question": "What does a CSS media query help a page do?", "choices": ["Adapt styles to conditions such as viewport width", "Create an HTML form", "Save a file to disk"], "answer": 0},
]
def admin_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin: abort(403)
        return f(*args, **kwargs)
    return inner

@bp.route("/")
def home(): return render_template("home.html", courses=Course.query.filter_by(published=True).all())
@bp.route("/courses")
def courses(): return render_template("courses.html", courses=Course.query.filter_by(published=True).all())
@bp.route("/courses/<slug>")
def course(slug):
    c = Course.query.filter_by(slug=slug, published=True).first_or_404()
    completed_lesson_ids = set()
    if current_user.is_authenticated:
        completed_lesson_ids = {
            progress.lesson_id
            for progress in LessonProgress.query.filter_by(user_id=current_user.id).all()
        }
    lessons = c.lessons()
    next_lesson = next((item for item in lessons if item.id not in completed_lesson_ids), lessons[0] if lessons else None)
    if current_user.is_authenticated and completed_lesson_ids:
        next_lesson = next((item for item in lessons if item.id not in completed_lesson_ids), next_lesson)
        if all(item.id in completed_lesson_ids for item in lessons):
            next_lesson = lessons[-1] if lessons else None
    passed_exam = current_user.is_authenticated and ExamAttempt.query.filter_by(user_id=current_user.id, course_id=c.id, passed=True).first() is not None
    existing_certificate = Certificate.query.filter_by(user_id=current_user.id, course_id=c.id).first() if current_user.is_authenticated else None
    response = make_response(render_template("course.html", course=c, modules=c.learning_modules(), completed_lesson_ids=completed_lesson_ids, next_lesson=next_lesson, passed_exam=passed_exam, existing_certificate=existing_certificate))
    if current_user.is_authenticated:
        response.headers["Cache-Control"] = "private, no-store"
    return response
@bp.post("/courses/<slug>/enroll")
@login_required
def enroll(slug):
    c = Course.query.filter_by(slug=slug, published=True).first_or_404()
    if c not in current_user.enrollments: current_user.enrollments.append(c); db.session.commit(); flash("You’re enrolled. Let’s build something.", "success")
    return redirect(url_for("main.course", slug=slug))
@bp.route("/courses/<course_slug>/<lesson_slug>")
def lesson(course_slug, lesson_slug):
    c = Course.query.filter_by(slug=course_slug).first_or_404()
    all_lessons = c.lessons()
    l = next((x for x in all_lessons if x.slug == lesson_slug), None)
    if not l: abort(404)
    saved_draft = None
    completed_lesson_ids = set()
    if current_user.is_authenticated:
        draft = LessonDraft.query.filter_by(user_id=current_user.id, lesson_id=l.id).first()
        if draft:
            try:
                saved_draft = json.loads(draft.code_json)
            except (TypeError, ValueError):
                saved_draft = None
        completed_lesson_ids = {
            p.lesson_id for p in LessonProgress.query.filter_by(user_id=current_user.id).all()
        }
    lesson_index = next((i for i, x in enumerate(all_lessons) if x.id == l.id), 0)
    total_lessons = len(all_lessons)
    prev_lesson = all_lessons[lesson_index - 1] if lesson_index > 0 else None
    next_lesson = all_lessons[lesson_index + 1] if lesson_index + 1 < total_lessons else None
    learning_modules = c.learning_modules()
    response = make_response(render_template(
        "lesson.html",
        course=c,
        lesson=l,
        lessons=all_lessons,
        modules=learning_modules,
        saved_draft=saved_draft,
        completed_lesson_ids=completed_lesson_ids,
        lesson_index=lesson_index,
        total_lessons=total_lessons,
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
    ))
    if current_user.is_authenticated:
        response.headers["Cache-Control"] = "private, no-store"
    return response

@bp.post("/api/lessons/<int:lesson_id>/draft")
@login_required
def save_lesson_draft(lesson_id):
    lesson = db.session.get(Lesson, lesson_id) or abort(404)
    payload = request.get_json(silent=True) or {}
    draft = payload.get("draft")
    if not isinstance(draft, dict) or any(not isinstance(value, str) for value in draft.values()):
        return jsonify(ok=False, error="invalid_draft"), 400
    if len(json.dumps(draft)) > 100_000:
        return jsonify(ok=False, error="draft_too_large"), 413
    saved = LessonDraft.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()
    if saved is None:
        saved = LessonDraft(user_id=current_user.id, lesson_id=lesson.id)
        db.session.add(saved)
    saved.code_json = json.dumps(draft)
    db.session.commit()
    return jsonify(ok=True)
@bp.post("/api/lessons/<int:lesson_id>/complete")
def complete_lesson(lesson_id):
    if not current_user.is_authenticated:
        lesson = db.session.get(Lesson, lesson_id) or abort(404)
        return jsonify(ok=False, error="login_required", login_url=url_for("main.login", next=url_for("main.lesson", course_slug=lesson.module.course.slug, lesson_slug=lesson.slug))), 401
    lesson = db.session.get(Lesson, lesson_id) or abort(404)
    if not LessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first():
        db.session.add(LessonProgress(user=current_user, lesson=lesson)); current_user.xp += 10; db.session.commit()
    lessons = lesson.module.course.lessons()
    lesson_index = next((index for index, item in enumerate(lessons) if item.id == lesson.id), -1)
    next_url = None
    if lesson_index >= 0 and lesson_index + 1 < len(lessons):
        next_lesson = lessons[lesson_index + 1]
        next_url = url_for("main.lesson", course_slug=lesson.module.course.slug, lesson_slug=next_lesson.slug)
    else:
        next_url = url_for("main.course", slug=lesson.module.course.slug)
    return jsonify(ok=True, xp=current_user.xp, next_url=next_url)
@bp.post("/api/quiz/<int:lesson_id>/submit")
@login_required
def quiz(lesson_id):
    lesson = db.session.get(Lesson, lesson_id) or abort(404)
    answer = str(request.json.get("answer", "")).strip().lower()
    expected = str(getattr(lesson, "quiz_answer", "")).strip().lower()
    correct = bool(expected) and answer == expected
    if correct:
        current_user.xp += 5
        db.session.commit()
    return jsonify(correct=correct, answer=expected, explanation="Review the lesson example and connect the concept to the code you wrote.")
@bp.route("/challenges")
def challenges(): return render_template("challenges.html", challenges=Challenge.query.all())
@bp.route("/challenges/<slug>")
def challenge(slug): return render_template("challenge.html", challenge=Challenge.query.filter_by(slug=slug).first_or_404())
@bp.post("/api/challenges/<int:challenge_id>/submit")
@login_required
def submit_challenge(challenge_id):
    c = db.session.get(Challenge, challenge_id) or abort(404); code = request.json.get("code", "")
    passed = c.expected_fragment.replace(" ", "") in code.replace(" ", "")
    if passed: current_user.xp += c.points; db.session.commit()
    return jsonify(passed=passed, message="Nice work — your solution meets the public contract." if passed else "Not quite. Check the function name and required return value.")
@bp.route("/projects")
def projects(): return render_template("projects.html", projects=Project.query.all())
@bp.route("/projects/<slug>")
def project(slug): return render_template("project.html", project=Project.query.filter_by(slug=slug).first_or_404())
@bp.route("/dashboard")
@login_required
def dashboard():
    certificates = Certificate.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", certificates=certificates, enrolled=current_user.enrollments)

@bp.post("/api/user/update")
@login_required
def update_profile():
    name = request.form.get("name", "").strip()
    avatar_url = request.form.get("avatar_url", "").strip()
    if name:
        current_user.name = name
    if avatar_url:
        current_user.avatar_url = avatar_url
    db.session.commit()
    flash("Profile updated successfully.", "success")
    return redirect(url_for("main.dashboard"))
@bp.post("/courses/<slug>/certificate")
@login_required
def certificate(slug):
    c = Course.query.filter_by(slug=slug).first_or_404()
    lessons = c.lessons()
    completed_ids = {
        progress.lesson_id
        for progress in LessonProgress.query.filter_by(user_id=current_user.id).all()
    }
    if not lessons or any(lesson.id not in completed_ids for lesson in lessons):
        flash("Complete every lesson before claiming your certificate.", "error")
        return redirect(url_for("main.course", slug=slug))
    if not ExamAttempt.query.filter_by(user_id=current_user.id, course_id=c.id, passed=True).first():
        flash("Pass the final course exam before claiming your certificate.", "error")
        return redirect(url_for("main.exam", slug=slug))
    cert = Certificate.query.filter_by(user_id=current_user.id, course_id=c.id).first()
    if not cert: cert = Certificate(certificate_id=f"CFA-{datetime.utcnow():%Y}-{uuid.uuid4().hex[:6].upper()}", user=current_user, course=c); db.session.add(cert); db.session.commit()
    return redirect(url_for("main.verify", certificate_id=cert.certificate_id))

@bp.route("/courses/<slug>/exam", methods=["GET", "POST"])
@login_required
def exam(slug):
    c = Course.query.filter_by(slug=slug, published=True).first_or_404()
    lessons = c.lessons()
    completed_ids = {p.lesson_id for p in LessonProgress.query.filter_by(user_id=current_user.id).all()}
    if not lessons or any(item.id not in completed_ids for item in lessons):
        flash("Finish every course lesson before taking the final exam.", "error")
        return redirect(url_for("main.course", slug=slug))
    result = None
    if request.method == "POST":
        score = sum(1 for index, item in enumerate(COURSE_EXAM, 1) if request.form.get(f"q{index}") == str(item["answer"]))
        percent = round(score / len(COURSE_EXAM) * 100)
        passed = percent >= 70
        db.session.add(ExamAttempt(user_id=current_user.id, course_id=c.id, score=percent, passed=passed))
        db.session.commit()
        result = {"score": percent, "passed": passed}
    return render_template("exam.html", course=c, questions=COURSE_EXAM, result=result)
@bp.route("/verify/<certificate_id>")
def verify(certificate_id): return render_template("verify.html", certificate=Certificate.query.filter_by(certificate_id=certificate_id).first_or_404())
@bp.route("/blog")
def blog(): return render_template("blog.html", articles=Article.query.order_by(Article.published_at.desc()).all())
@bp.route("/blog/<slug>")
def article(slug): return render_template("article.html", article=Article.query.filter_by(slug=slug).first_or_404())
@bp.route("/search")
def search():
    q=request.args.get("q", "").strip(); results=[]
    if q: results = [("Course", x.title, url_for("main.course", slug=x.slug), x.description) for x in Course.query.filter(Course.title.ilike(f"%{q}%")).all()] + [("Article", x.title, url_for("main.article", slug=x.slug), x.excerpt) for x in Article.query.filter(Article.title.ilike(f"%{q}%")).all()]
    return render_template("search.html", q=q, results=results)
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user=User.query.filter_by(email=request.form.get("email", "").lower()).first()
        if user and user.check_password(request.form.get("password", "")): login_user(user); return redirect(request.args.get("next") or url_for("main.dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("auth.html", mode="login")
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name=request.form.get("name", "").strip(); email=request.form.get("email", "").lower().strip(); password=request.form.get("password", "")
        if len(name)<2 or "@" not in email or len(password)<8: flash("Use your name, a valid email, and a password of at least 8 characters.", "error")
        elif User.query.filter_by(email=email).first(): flash("An account with that email already exists.", "error")
        else:
            user=User(name=name, email=email); user.set_password(password); db.session.add(user); db.session.commit(); login_user(user); return redirect(url_for("main.dashboard"))
    return render_template("auth.html", mode="register")
@bp.post("/logout")
@login_required
def logout(): logout_user(); flash("You have been logged out.", "success"); return redirect(url_for("main.home"))
@bp.route("/admin")
@admin_required
def admin(): return render_template("admin.html", users=User.query.count(), courses=Course.query.count(), lessons=Lesson.query.count(), challenges=Challenge.query.count())
@bp.get("/api/courses")
def api_courses(): return jsonify([{"title":c.title,"slug":c.slug,"difficulty":c.difficulty,"duration":c.duration} for c in Course.query.filter_by(published=True)])
@bp.get("/api/courses/<slug>")
def api_course(slug):
    c=Course.query.filter_by(slug=slug).first_or_404(); return jsonify(title=c.title, description=c.description, modules=[{"title":m.title,"lessons":[l.title for l in m.lessons]} for m in c.modules])
@bp.route("/about")
@bp.route("/contact")
@bp.route("/privacy")
@bp.route("/terms")
@bp.route("/cookies")
def pages(): return render_template("page.html", page=request.path.strip("/") or "about")
@bp.route("/robots.txt")
def robots(): return make_response(f"User-agent: *\nAllow: /\nDisallow: /dashboard\nDisallow: /admin\nSitemap: {request.url_root}sitemap.xml\n", 200, {"Content-Type":"text/plain"})
@bp.get("/sw.js")
def service_worker():
    response = make_response(send_from_directory(current_app.static_folder, "sw.js"))
    response.headers["Content-Type"] = "application/javascript; charset=utf-8"
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response
@bp.get("/offline")
def offline_page():
    return send_from_directory(current_app.static_folder, "offline.html")
@bp.route("/sitemap.xml")
def sitemap(): return current_app.response_class(render_template("sitemap.xml", courses=Course.query.filter_by(published=True).all(), articles=Article.query.all()), mimetype="application/xml")
@bp.get("/google7d947423d6c5618b.html")
def google_verification():
    return current_app.response_class(
        "google-site-verification: google7d947423d6c5618b.html",
        mimetype="text/html"
    )