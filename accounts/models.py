from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", _("Student")
        TEACHER = "teacher", _("Teacher")
        ADMIN = "admin", _("Administrator")

    role = models.CharField(
        _("role"), max_length=20, choices=Role.choices, default=Role.STUDENT
    )
    phone = models.CharField(_("phone number"), max_length=20, blank=True)
    bio = models.TextField(_("biography"), blank=True)

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    def __str__(self):
        return self.get_full_name() or self.username
