import unittest

from app import create_app, db
from app.models import Certificate, Course, ExamAttempt, LessonDraft, LessonProgress, User
from app.routes import COURSE_EXAM


class LearningFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", "SECRET_KEY": "test-secret"})

    def setUp(self):
        self.client = self.app.test_client()
        with self.app.app_context():
            user = User(name="Learner", email=f"learner-{User.query.count()}@example.test")
            user.set_password("safe-test-password")
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id
            self.course_id = Course.query.filter_by(slug="responsive-web-design").one().id
            self.lessons = Course.query.get(self.course_id).lessons()
        with self.client.session_transaction() as session:
            session["_user_id"] = str(self.user_id)
            session["_fresh"] = True

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()

    def complete_course(self):
        with self.app.app_context():
            for lesson in self.lessons:
                if not LessonProgress.query.filter_by(user_id=self.user_id, lesson_id=lesson.id).first():
                    db.session.add(LessonProgress(user_id=self.user_id, lesson_id=lesson.id))
            db.session.commit()

    def test_html_first_path_and_typing_lesson(self):
        course_page = self.client.get("/courses/responsive-web-design")
        self.assertEqual(course_page.status_code, 200)
        self.assertIn(b"HTML from Scratch: Build the Page Structure", course_page.data)
        self.assertNotIn(b"Start Here: Computer and Web Basics", course_page.data)
        lesson = next(item for item in self.lessons if item.slug == "start-html-typing-basics")
        page = self.client.get(f"/courses/responsive-web-design/{lesson.slug}")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"index.html", page.data)
        self.assertIn(b'id="live-preview"', page.data)
        self.assertNotIn(b"Study this code", page.data)
        self.assertIn(b'id="lesson-sidebar"', page.data)
        self.assertIn(b"Run the Tests", page.data)
        self.assertIn(b"Step", page.data)
        self.assertIn(b"Previous", page.data)
        self.assertIn(b"Next", page.data)

    def test_css_lesson_has_blank_practice_and_preview(self):
        lesson = next(item for item in self.lessons if item.slug == "start-css-what-css-does")
        page = self.client.get(f"/courses/responsive-web-design/{lesson.slug}")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"styles.css", page.data)
        self.assertNotIn(b"CSS Example", page.data)
        self.assertIn(b'id="live-preview"', page.data)

    def test_draft_autosave_restores_account_code(self):
        lesson = self.lessons[0]
        draft = {"code": "<h1>Do not clear my work</h1>"}
        self.assertEqual(self.client.post(f"/api/lessons/{lesson.id}/draft", json={"draft": draft}).status_code, 200)
        page = self.client.get(f"/courses/responsive-web-design/{lesson.slug}")
        self.assertIn(b"Do not clear my work", page.data)
        with self.app.app_context():
            self.assertTrue(LessonDraft.query.filter_by(user_id=self.user_id, lesson_id=lesson.id).one())

    def test_completion_is_idempotent(self):
        lesson = self.lessons[0]
        self.assertEqual(self.client.post(f"/api/lessons/{lesson.id}/complete").status_code, 200)
        self.assertEqual(self.client.post(f"/api/lessons/{lesson.id}/complete").status_code, 200)
        with self.app.app_context():
            self.assertEqual(LessonProgress.query.filter_by(user_id=self.user_id, lesson_id=lesson.id).count(), 1)
            self.assertEqual(db.session.get(User, self.user_id).xp, 10)

    def test_certificate_requires_exam_and_verifies(self):
        self.complete_course()
        blocked = self.client.post("/courses/responsive-web-design/certificate")
        self.assertIn("/exam", blocked.headers["Location"])
        exam = self.client.get("/courses/responsive-web-design/exam")
        self.assertEqual(exam.status_code, 200)
        answers = {f"q{index}": str(item["answer"]) for index, item in enumerate(COURSE_EXAM, 1)}
        passed = self.client.post("/courses/responsive-web-design/exam", data=answers)
        self.assertIn(b"You passed!", passed.data)
        claimed = self.client.post("/courses/responsive-web-design/certificate")
        verified = self.client.get(claimed.headers["Location"])
        self.assertEqual(verified.status_code, 200)
        self.assertIn(b"Certificate verified", verified.data)
        with self.app.app_context():
            self.assertEqual(Certificate.query.filter_by(user_id=self.user_id).count(), 1)
            self.assertTrue(ExamAttempt.query.filter_by(user_id=self.user_id, passed=True).first())

    def test_exam_rejects_incomplete_course(self):
        response = self.client.get("/courses/responsive-web-design/exam")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/courses/responsive-web-design", response.headers["Location"])

    def test_seo_and_pwa_endpoints(self):
        self.assertEqual(self.client.get("/robots.txt").status_code, 200)
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)
        self.assertEqual(self.client.get("/static/manifest.json").status_code, 200)
        worker = self.client.get("/sw.js")
        self.assertEqual(worker.status_code, 200)
        self.assertEqual(worker.headers.get("Service-Worker-Allowed"), "/")


if __name__ == "__main__":
    unittest.main()
