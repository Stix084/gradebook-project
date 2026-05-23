from django.db import models


# ---------------------------------
# COURSE MODEL
# ---------------------------------
class Course(models.Model):
        name = models.CharField(max_length=200)
        code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.code} - {self.name}"


# ---------------------------------
# ASSESSMENT MODEL
# ---------------------------------
class Assessment(models.Model):
    QUIZ = "QUIZ"
    ASSIGNMENT = "ASSIGNMENT"
    MIDTERM = "MIDTERM"
    FINAL = "FINAL"
    OTHER = "OTHER"

    TYPE_CHOICES = [
        (QUIZ, "Quiz"),
        (ASSIGNMENT, "Assignment"),
        (MIDTERM, "Midterm"),
        (FINAL, "Final Exam"),
        (OTHER, "Other"),
    ]

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="assessments"
    )
    title = models.CharField(max_length=100)
    assessment_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=OTHER
    )
    total_marks = models.IntegerField()
    weight = models.FloatField(
        default=0,
        help_text="Percentage contribution toward final mark"
    )

    def __str__(self):
        return f"{self.course.code} - {self.title}"


# ---------------------------------
# GRADE MODEL
# ---------------------------------
class Grade(models.Model):
    student = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE
    )

    marks_obtained = models.FloatField()

    class Meta:
        unique_together = ("student", "assessment")

    def __str__(self):
        return f"{self.student} - {self.assessment}"