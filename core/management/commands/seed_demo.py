from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from courses.models import Course, Lesson, Module

User = get_user_model()

COURSES = [
    {
        "title": "Web Development (Frontend)",
        "slug": "web-frontend",
        "short_description": "HTML, CSS, JavaScript and React — build modern websites from scratch.",
        "duration_weeks": 16,
        "price": 1200000,
        "modules": [
            ("Basics of the Web", ["How the internet works", "HTML structure", "CSS styling"]),
            ("JavaScript", ["Variables and types", "Functions", "DOM manipulation"]),
        ],
    },
    {
        "title": "Graphic Design",
        "slug": "graphic-design",
        "short_description": "Photoshop, Illustrator and Figma — from idea to professional design.",
        "duration_weeks": 12,
        "price": 900000,
        "modules": [
            ("Design Foundations", ["Color theory", "Typography", "Composition"]),
        ],
    },
    {
        "title": "Computer Literacy",
        "slug": "computer-literacy",
        "short_description": "Windows, Word, Excel and the internet — essential office skills.",
        "duration_weeks": 8,
        "price": 0,
        "modules": [
            ("Getting Started", ["Operating system basics", "Working with files", "Internet safety"]),
        ],
    },
]


class Command(BaseCommand):
    help = "Seed demo data: an admin, a teacher, and sample published courses."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin", "admin@example.com", "admin12345", role=User.Role.ADMIN
            )
            self.stdout.write("Created superuser admin / admin12345")

        teacher, created = User.objects.get_or_create(
            username="teacher_aziz",
            defaults={
                "first_name": "Aziz",
                "last_name": "Karimov",
                "role": User.Role.TEACHER,
                "bio": "Senior developer with 8 years of industry experience.",
            },
        )
        if created:
            teacher.set_password("teacher12345")
            teacher.save()
            self.stdout.write("Created teacher teacher_aziz / teacher12345")

        for data in COURSES:
            course, created = Course.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "short_description": data["short_description"],
                    "duration_weeks": data["duration_weeks"],
                    "price": data["price"],
                    "teacher": teacher,
                    "is_published": True,
                    "is_featured": True,
                },
            )
            if created:
                for m_order, (m_title, lessons) in enumerate(data["modules"]):
                    module = Module.objects.create(
                        course=course, title=m_title, order=m_order
                    )
                    for l_order, l_title in enumerate(lessons):
                        Lesson.objects.create(
                            module=module, title=l_title, order=l_order,
                            content=f"Lesson materials for: {l_title}",
                        )
                self.stdout.write(f"Created course: {course.title}")

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
