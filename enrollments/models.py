from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from courses.models import Course
from users.models import User



class Enrollment(models.Model):
   # ACTIVE = "active"
   # WITHDRAWN = "withdrawn"
   # COMPLETED = "completed"


    ACTIVE  = "ACTIVE"
    SUBMITTED = "SUBMITTED"
    COMPLETED = "COMPLETED"

    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (SUBMITTED, "Submitted"),
        (COMPLETED, "Completed"),
    ]

 # STATUS_CHOICES = [
 #       (ACTIVE, "Active"),
 #       (WITHDRAWN, "Withdrawn"),
 #       (COMPLETED, "Completed"),
 #   ]


   

#STATUS_CHOICES = (
#        ("ACTIVE", "Active"),
#        ("SUBMITTED", "Submitted for Approval"),
#        ("APPROVED", "Approved"),
#        ("COMPLETED", "Completed"),
#    )


    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    '''
    is_locked = models.BooleanField(
        default=False,
        help_text="Locks final mark and prevents further grade changes"
    )
    '''
    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} → {self.course}"
    

    def final_mark(self):
        return self.course.calculate_final_mark(self)

'''

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("SUBMITTED", "Submitted for Approval"),
        ("APPROVED", "Approved"),
        ("COMPLETED", "Completed"),
    )

    student = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    is_locked = models.BooleanField(default=False)

    approved_by = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="approved_enrollments"
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    def final_mark(self):
        return self.course.calculate_final_mark(self)

    def __str__(self):
        return f"{self.student} - {self.course}"

'''
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())