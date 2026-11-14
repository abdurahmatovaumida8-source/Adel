from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), unique=True)
    short_description = models.CharField(_("short description"), max_length=300)
    description = models.TextField(_("full description"), blank=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("teacher"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses_taught",
        limit_choices_to={"role": "teacher"},
    )
    duration_weeks = models.PositiveIntegerField(_("duration (weeks)"), default=12)
    price = models.DecimalField(
        _("price (UZS)"), max_digits=12, decimal_places=0, default=0
    )
    is_published = models.BooleanField(_("published"), default=False)
    is_featured = models.BooleanField(_("featured on landing page"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "title"]
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules"
    )
    title = models.CharField(_("title"), max_length=200)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = _("module")
        verbose_name_plural = _("modules")

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(_("title"), max_length=200)
    content = models.TextField(_("content"), blank=True)
    video_url = models.URLField(_("video URL"), blank=True)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = _("lesson")
        verbose_name_plural = _("lessons")

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")
        verbose_name = _("enrollment")
        verbose_name_plural = _("enrollments")

    def __str__(self):
        return f"{self.student} → {self.course}"

    @property
    def progress_percent(self):
        total = Lesson.objects.filter(module__course=self.course).count()
        if not total:
            return 0
        done = LessonProgress.objects.filter(
            student=self.student, lesson__module__course=self.course
        ).count()
        return round(done * 100 / total)


class LessonProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="progress"
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "lesson")
        verbose_name = _("lesson progress")
        verbose_name_plural = _("lesson progress")

    def __str__(self):
        return f"{self.student} ✓ {self.lesson}"
