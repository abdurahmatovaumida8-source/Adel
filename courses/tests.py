from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Course, Enrollment, Lesson, Module

User = get_user_model()


class PlatformSmokeTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            "teacher1", password="pass12345", role=User.Role.TEACHER
        )
        self.student = User.objects.create_user(
            "student1", password="pass12345", role=User.Role.STUDENT
        )
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_description="Short",
            teacher=self.teacher,
            is_published=True,
            is_featured=True,
        )
        module = Module.objects.create(course=self.course, title="M1")
        self.lesson = Lesson.objects.create(module=module, title="L1")

    def test_landing_page_renders(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course")

    def test_landing_application_form_submits(self):
        response = self.client.post(
            reverse("core:home"),
            {"full_name": "Ali Valiyev", "phone": "+998901234567"},
        )
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("courses:dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_student_registration_and_dashboard(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newstudent",
                "first_name": "New",
                "last_name": "Student",
                "password1": "complex-pass-123",
                "password2": "complex-pass-123",
            },
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("courses:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_enroll_and_complete_lesson(self):
        self.client.login(username="student1", password="pass12345")
        self.client.post(reverse("courses:enroll", args=[self.course.slug]))
        enrollment = Enrollment.objects.get(student=self.student, course=self.course)
        self.assertEqual(enrollment.progress_percent, 0)
        self.client.post(
            reverse("courses:complete_lesson", args=[self.course.slug, self.lesson.id])
        )
        self.assertEqual(enrollment.progress_percent, 100)

    def test_lesson_locked_without_enrollment(self):
        self.client.login(username="student1", password="pass12345")
        response = self.client.get(
            reverse("courses:lesson_detail", args=[self.course.slug, self.lesson.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_russian_translation_active(self):
        response = self.client.get("/ru/")
        self.assertContains(response, "Курсы")
