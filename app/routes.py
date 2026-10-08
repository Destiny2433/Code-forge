from datetime import datetime
import uuid
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, abort, current_app, make_response
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from . import db, limiter
from .models import User, Course, Lesson, LessonProgress, Enrollment, Challenge, Project, Certificate, Article

bp = Blueprint("main", __name__)
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
    return render_template("course.html", course=c, completed_lesson_ids=completed_lesson_ids)
@bp.post("/courses/<slug>/enroll")
@login_required
def enroll(slug):
    c = Course.query.filter_by(slug=slug, published=True).first_or_404()
    if c not in current_user.enrollments: current_user.enrollments.append(c); db.session.commit(); flash("You’re enrolled. Let’s build something.", "success")
    return redirect(url_for("main.course", slug=slug))
@bp.route("/courses/<course_slug>/<lesson_slug>")
def lesson(course_slug, lesson_slug):
    c = Course.query.filter_by(slug=course_slug).first_or_404()
    l = next((x for x in c.lessons() if x.slug == lesson_slug), None)
    if not l: abort(404)
    return render_template("lesson.html", course=c, lesson=l, lessons=c.lessons())
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
    if c.progress_for(current_user) < 100: flash("Complete every lesson before claiming your certificate.", "error"); return redirect(url_for("main.course", slug=slug))
    cert = Certificate.query.filter_by(user_id=current_user.id, course_id=c.id).first()
    if not cert: cert = Certificate(certificate_id=f"CFA-{datetime.utcnow():%Y}-{uuid.uuid4().hex[:6].upper()}", user=current_user, course=c); db.session.add(cert); db.session.commit()
    return redirect(url_for("main.verify", certificate_id=cert.certificate_id))
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
@limiter.limit("10 per minute")
def login():
    if request.method == "POST":
        user=User.query.filter_by(email=request.form.get("email", "").lower()).first()
        if user and user.check_password(request.form.get("password", "")): login_user(user); return redirect(request.args.get("next") or url_for("main.dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("auth.html", mode="login")
@bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
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
def robots(): return make_response("User-agent: *\nAllow: /\nDisallow: /dashboard\nDisallow: /admin\nSitemap: /sitemap.xml\n", 200, {"Content-Type":"text/plain"})
@bp.route("/sitemap.xml")
def sitemap(): return current_app.response_class(render_template("sitemap.xml", courses=Course.query.all(), articles=Article.query.all()), mimetype="application/xml")
