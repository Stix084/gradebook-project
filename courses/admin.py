from django.contrib import admin
from .models import Course, Assessment, Grade


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "lecturer")
    search_fields = ("code", "name")
    list_filter = ("lecturer",)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("course", "title", "assessment_type", "total_marks", "weight")
    list_filter = ("course", "assessment_type")
    search_fields = ("title",)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "assessment", "marks_obtained")
    list_filter = ("assessment",)
    actions = ["reset_grades"]

    def reset_grades(self, request, queryset):
        queryset.update(marks_obtained=0)
    reset_grades.short_description = "Reset selected grades"