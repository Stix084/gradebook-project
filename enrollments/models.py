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

    def final_mark(self):
        from courses.models import Grade
        grades = Grade.objects.filter(
            student=self.student,
            assessment__course=self.course
        ).select_related("assessment")

        final = 0

        assignments = [g for g in grades if g.assessment.assessment_type == "ASSIGNMENT"]
        others = [g for g in grades if g.assessment.assessment_type != "ASSIGNMENT"]

        for g in others:
            if g.assessment.total_marks > 0:
                ratio = g.marks_obtained / g.assessment.total_marks
                final += ratio * g.assessment.weight

        if assignments:
            total_obtained = sum(g.marks_obtained for g in assignments)
            total_possible = sum(g.assessment.total_marks for g in assignments)
            group_weight = assignments[0].assessment.weight
            if total_possible > 0:
                final += (total_obtained / total_possible) * group_weight

        return round(final, 1)