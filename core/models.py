from django.db import models
from django.utils.translation import gettext_lazy as _


class Application(models.Model):
    """Enrollment request submitted from the public landing page."""

    class Status(models.TextChoices):
        NEW = "new", _("New")
        CONTACTED = "contacted", _("Contacted")
        ENROLLED = "enrolled", _("Enrolled")
        REJECTED = "rejected", _("Rejected")

    full_name = models.CharField(_("full name"), max_length=200)
    phone = models.CharField(_("phone number"), max_length=20)
    course = models.ForeignKey(
        "courses.Course",
        verbose_name=_("course of interest"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    message = models.TextField(_("message"), blank=True)
    status = models.CharField(
        _("status"), max_length=20, choices=Status.choices, default=Status.NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("application")
        verbose_name_plural = _("applications")

    def __str__(self):
        return f"{self.full_name} ({self.phone})"
