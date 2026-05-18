from django.contrib.auth.models import AbstractUser
from django.db import models
# from users.models import User


class User(AbstractUser):
    ROLE_CHOICES = (
        ("LECTURER", "Lecturer"),
        ("STUDENT", "Student"),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="STUDENT",
    )

    student_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username



