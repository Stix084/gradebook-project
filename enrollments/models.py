from django.db import models
from courses.models import Course
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
        Course,
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
        default=False,
        help_text="Locks final mark and prevents further grade changes"
    )

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} → {self.course}"

    def final_mark(self):
        return self.course.calculate_final_mark(self)