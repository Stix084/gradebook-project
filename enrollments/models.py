from django.db import models
from users.models import User


class Enrollment(models.Model):

    ACTIVE = "ACTIVE"
    SUBMITTED = "SUBMITTED"
    COMPLETED = "COMPLETED"

    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (SUBMITTED, "Submitted"),
        (COMPLETED, "Completed"),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

    is_locked = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} → {self.course}"