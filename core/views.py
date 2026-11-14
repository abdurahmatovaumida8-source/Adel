from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from courses.models import Course, Enrollment

from .forms import ApplicationForm

User = get_user_model()


def home(request):
    featured = Course.objects.filter(is_published=True, is_featured=True)[:6]
    teachers = User.objects.filter(role="teacher", is_active=True)[:8]
    stats = {
        "courses": Course.objects.filter(is_published=True).count(),
        "students": User.objects.filter(role="student").count(),
        "teachers": User.objects.filter(role="teacher").count(),
        "enrollments": Enrollment.objects.count(),
    }
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("Thank you! We received your application and will call you soon.")
            )
            return redirect("core:home")
    else:
        form = ApplicationForm()
    return render(
        request,
        "core/home.html",
        {"featured": featured, "teachers": teachers, "stats": stats, "form": form},
    )
