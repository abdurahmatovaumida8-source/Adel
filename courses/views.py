from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Enrollment, Lesson, LessonProgress


@login_required
def dashboard(request):
    enrollments = (
        Enrollment.objects.filter(student=request.user)
        .select_related("course", "course__teacher")
    )
    enrolled_ids = [e.course_id for e in enrollments]
    available = Course.objects.filter(is_published=True).exclude(id__in=enrolled_ids)
    return render(
        request,
        "courses/dashboard.html",
        {"enrollments": enrollments, "available_courses": available},
    )


@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment = Enrollment.objects.filter(
        student=request.user, course=course
    ).first()
    completed_ids = set(
        LessonProgress.objects.filter(
            student=request.user, lesson__module__course=course
        ).values_list("lesson_id", flat=True)
    )
    modules = course.modules.prefetch_related("lessons")
    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "enrollment": enrollment,
            "modules": modules,
            "completed_ids": completed_ids,
        },
    )


@login_required
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    if request.method == "POST":
        Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect("courses:course_detail", slug=slug)


@login_required
def lesson_detail(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        return redirect("courses:course_detail", slug=slug)
    completed = LessonProgress.objects.filter(
        student=request.user, lesson=lesson
    ).exists()
    return render(
        request,
        "courses/lesson_detail.html",
        {"course": course, "lesson": lesson, "completed": completed},
    )


@login_required
def complete_lesson(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    if request.method == "POST" and Enrollment.objects.filter(
        student=request.user, course=course
    ).exists():
        LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)
    return redirect("courses:lesson_detail", slug=slug, lesson_id=lesson_id)
