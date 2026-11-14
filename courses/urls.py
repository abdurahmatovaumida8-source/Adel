from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("course/<slug:slug>/", views.course_detail, name="course_detail"),
    path("course/<slug:slug>/enroll/", views.enroll, name="enroll"),
    path(
        "course/<slug:slug>/lesson/<int:lesson_id>/",
        views.lesson_detail,
        name="lesson_detail",
    ),
    path(
        "course/<slug:slug>/lesson/<int:lesson_id>/complete/",
        views.complete_lesson,
        name="complete_lesson",
    ),
]
