from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class Enrollment(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), primary_key=True)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    avatar_url = db.Column(db.String(500), nullable=True)
    xp = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrollments = db.relationship("Course", secondary="enrollment", back_populates="students")
    progress = db.relationship("LessonProgress", backref="user", cascade="all, delete-orphan")
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
    @property
    def streak(self):
        days = {p.completed_at.date() for p in self.progress if p.completed_at}
        cur, total = date.today(), 0
        while cur in days: total += 1; cur = date.fromordinal(cur.toordinal()-1)
        return total

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(30), default="Beginner")
    duration = db.Column(db.String(40), default="6 hours")
    category = db.Column(db.String(60), default="Programming")
    instructor = db.Column(db.String(80), default="HiveryTech Team")
    published = db.Column(db.Boolean, default=True)
    modules = db.relationship("Module", backref="course", cascade="all, delete-orphan", order_by="Module.position")
    students = db.relationship("User", secondary="enrollment", back_populates="enrollments")
    projects = db.relationship("Project", backref="course", lazy=True)
    def lessons(self): return [l for m in self.modules for l in m.lessons]
    def progress_for(self, user):
        total = len(self.lessons())
        done = sum(1 for p in user.progress if p.lesson in self.lessons()) if user.is_authenticated else 0
        return round(done / total * 100) if total else 0

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    position = db.Column(db.Integer, default=1)
    lessons = db.relationship("Lesson", backref="module", cascade="all, delete-orphan", order_by="Lesson.position")

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(180), nullable=False)
    body = db.Column(db.Text, nullable=False)
    example_code = db.Column(db.Text, default="")
    code = db.Column(db.Text, default="")
    language = db.Column(db.String(20), default="python")
    position = db.Column(db.Integer, default=1)
    tests = db.Column(db.Text, default="[]")
    hints = db.Column(db.Text, default="[]")
    __table_args__ = (db.UniqueConstraint("module_id", "slug", name="unique_lesson_slug"),)

class LessonProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    lesson = db.relationship("Lesson")
    __table_args__ = (db.UniqueConstraint("user_id", "lesson_id", name="unique_lesson_progress"),)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(20), default="python")
    difficulty = db.Column(db.String(30), default="Beginner")
    points = db.Column(db.Integer, default=20)
    expected_fragment = db.Column(db.String(160), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    title = db.Column(db.String(160), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False)
    difficulty = db.Column(db.String(30), default="Beginner")
    description = db.Column(db.Text, nullable=False)
    checklist = db.Column(db.Text, nullable=False)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    certificate_id = db.Column(db.String(40), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User"); course = db.relationship("Course")

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False)
    excerpt = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60), default="Programming")
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
