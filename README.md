# Tarmoqlararo Kasb-Hunar — Learning Academy Platform

Единая высокотехнологичная цифровая платформа, которая сочетает в себе
продающую витрину (Landing Page) для привлечения новых студентов и закрытую
экосистему (Web-приложение / LMS) для автоматизации обучения и управления
процессами академии.

Built with **Django 5** · Multilingual: **O'zbekcha / Русский / English**

## Features

### Public landing page (`/`)
- Hero section with live academy statistics
- Featured courses showcase with prices and duration
- "Why study with us" and teachers sections
- Enrollment application form (saved to the database, managed in admin)
- Language switcher: UZ (default) / RU / EN

### LMS (`/learn/`)
- Student self-registration and login (`/accounts/`)
- Student dashboard: enrolled courses with progress bars + course catalog
- Course pages with modules and lessons (curriculum)
- Lesson pages with video embed + text content and "Mark as completed"
- Automatic progress tracking per student

### Administration (`/admin/`)
- Manage courses, modules, lessons (inline editing)
- Process landing-page applications (statuses: new → contacted → enrolled)
- Manage users with roles: student / teacher / administrator
- View enrollments and lesson progress

## Quick start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py compilemessages   # build UZ/RU translations (needs gettext)
python manage.py seed_demo         # demo admin, teacher and 3 sample courses
python manage.py runserver
```

Then open:
- Landing page: http://127.0.0.1:8000/
- LMS dashboard: http://127.0.0.1:8000/learn/
- Admin panel: http://127.0.0.1:8000/admin/ (demo: `admin` / `admin12345`)

## Project structure

```
config/     project settings, root URLs (i18n-aware)
core/       landing page + enrollment applications
accounts/   custom User model with roles, registration/login
courses/    Course → Module → Lesson, Enrollment, LessonProgress
templates/  Tailwind-styled pages (base, landing, auth, LMS)
locale/     uz / ru translations
```

## Tests

```bash
python manage.py test
```

## Roadmap (next phases)

- [ ] Payments (Payme / Click) and paid enrollment
- [ ] Homework submissions and grading
- [ ] Teacher dashboard (outside Django admin)
- [ ] Attendance and schedule management
- [ ] Certificates (PDF generation)
- [ ] SMS/Telegram notifications for applications
