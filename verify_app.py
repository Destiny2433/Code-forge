from app import create_app

app = create_app()
client = app.test_client()

home = client.get('/')
course = client.get('/courses/responsive-web-design')

print('home_status=', home.status_code)
print('course_status=', course.status_code)
print('home_has_codeforge=', 'CodeForge' in home.get_data(as_text=True))
print('course_has_title=', 'Responsive Web Design Certification' in course.get_data(as_text=True))
print('course_has_start=', 'Start Learning' in course.get_data(as_text=True))
