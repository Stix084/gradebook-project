from django.contrib import admin
from .models import (
    Course,
    AssessmentComponent,
    AssessmentItem,
    Grade
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "lecturer", "academic_year")
    search_fields = ("code", "name")


@admin.register(AssessmentComponent)
class AssessmentComponentAdmin(admin.ModelAdmin):
    list_display = ("course", "name", "weight")


@admin.register(AssessmentItem)
class AssessmentItemAdmin(admin.ModelAdmin):
    list_display = ("name", "component", "max_score")


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "enrollment",
        "assessment_item",
        "score",
        "is_locked",
    )
    list_filter = ("is_locked", "assessment_item")

    actions = ["lock_grades"]

    def lock_grades(self, request, queryset):
        queryset.update(is_locked=True)

    lock_grades.short_description = "Lock selected grades"

