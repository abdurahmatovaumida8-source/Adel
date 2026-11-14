from django import forms
from django.utils.translation import gettext_lazy as _

from courses.models import Course

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("full_name", "phone", "course", "message")
        labels = {
            "full_name": _("Full name"),
            "phone": _("Phone number"),
            "course": _("Course of interest"),
            "message": _("Message"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(is_published=True)
        self.fields["course"].required = False
        self.fields["message"].required = False
