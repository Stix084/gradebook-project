from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    lecturer = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


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


class ClassLog(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="class_logs"
    )
    lecturer = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="class_logs"
    )
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text="Duration in hours e.g. 1.5"
    )
    topic = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.course.code} - {self.topic} ({self.date})"