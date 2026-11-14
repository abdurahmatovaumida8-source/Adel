from django.contrib import admin

from .models import Course, Enrollment, Lesson, LessonProgress, Module


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "price", "is_published", "is_featured")
    list_filter = ("is_published", "is_featured")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order")
    list_filter = ("module__course",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    list_filter = ("course",)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "completed_at")
