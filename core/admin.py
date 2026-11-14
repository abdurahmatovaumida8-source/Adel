from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "course", "status", "created_at")
    list_filter = ("status", "course")
    search_fields = ("full_name", "phone")
    list_editable = ("status",)
