from django.db import models
from users.models import User
from django.conf import settings

from django.core.exceptions import ValidationError


# Create your models here.


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)

    name = models.CharField(max_length=100)



    lecturer = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="courses_taught"
    )
    academic_year = models.CharField(
        max_length=9,
        help_text="Format: 2025/2026"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )


    
    def calculate_final_mark(self, enrollment):
        total = 0
        for component in self.components.all():
            total += component.calculate_score(enrollment)
        return round(total, 2)
    


    def __str__(self):
        return f"{self.code} - {self.name}"



# -----------------------------------------------------




class AssessmentComponent(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="components"
    )
    name = models.CharField(max_length=100)
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage contribution to final mark"
    )

    def calculate_score(self, enrollment):
        grades = Grade.objects.filter(
            enrollment=enrollment,
            assessment_item__component=self
        )

        if not grades.exists():
            return 0

        total_percentage = sum(
            grade.percentage() for grade in grades
        ) / grades.count()

        # scale to component weight
        return (total_percentage * self.weight) / 100

    def __str__(self):
        return f"{self.name} ({self.weight}%)"


#-----------------------------------------------------


class AssessmentItem(models.Model):
    component = models.ForeignKey(
        "courses.AssessmentComponent",
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=100)
    #max_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)

  #  max_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.component})"



#-------------------------------------------------------


'''
class Grade(models.Model):
    enrollment = models.ForeignKey(
        "enrollments.Enrollment",
        on_delete=models.CASCADE,
        related_name="grades"
    )
    assessment_item = models.ForeignKey(
        "courses.AssessmentItem",
        on_delete=models.CASCADE,
        related_name="grades"
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    is_locked = models.BooleanField(default=False)


    
    def percentage(self):
         if self.assessment_item.max_score == 0:
           return 0
         return (self.score / self.assessment_item.max_score) * 100


    def __str__(self):
        return f"{self.enrollment} - {self.assessment_item}"
    
    '''
    
 #   from django.core.exceptions import ValidationError

class Grade(models.Model):
    enrollment = models.ForeignKey(
        "enrollments.Enrollment",
        on_delete=models.CASCADE,
        related_name="grades"
    )
    assessment_item = models.ForeignKey(
        "courses.AssessmentItem",
        on_delete=models.CASCADE,
        related_name="grades"
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    is_locked = models.BooleanField(default=False) 

    def clean(self):
        if self.enrollment.is_locked:
            raise ValidationError("This enrollment is locked. Grades cannot be modified.")

        if self.score < 0 or self.score > self.max_score:
            raise ValidationError("Score must be within allowed range.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def percentage(self):
        if self.max_score == 0:
            return 0
        return (self.score / self.max_score) * 100

    
    def __str__(self):
        return f"{self.enrollment} - {self.assessment_item}"
    

    #-------------------------------------------------------------------------
class Assessment(models.Model):
    ASSESSMENT_TYPES = (
        ("ASSIGNMENT", "Assignment"),
        ("TEST", "Test"),
        ("EXAM", "Exam"),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assessments"
    )

    title = models.CharField(max_length=100)

    assessment_type = models.CharField(
        max_length=20,
        choices=ASSESSMENT_TYPES
    )

    total_marks = models.FloatField(default=100)

    weight = models.FloatField(
        help_text="Contribution percentage to final mark"
    )

    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class AssessmentGrade(models.Model):
    student = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE
    )

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="grades"
    )

    marks_obtained = models.FloatField()

    feedback = models.TextField(
        blank=True,
        null=True
    )

    graded_at = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        return (
            self.marks_obtained /
            self.assessment.total_marks
        ) * 100

    def weighted_score(self):
        return (
            self.percentage() *
            self.assessment.weight
        ) / 100

    def __str__(self):
        return (
            f"{self.student.username} - "
            f"{self.assessment.title}"
        )


