from django.contrib import admin
from .models import Enrollment

'''
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "final_mark_display",
        "enrolled_at",
    )

    list_filter = ("course",)
    search_fields = ("student__username", "student__email")
    ordering = ("course", "student")

    @admin.display(description="Final Mark")
    def final_mark_display(self, obj):
        try:
            return obj.final_mark()
        except Exception:
            return "-"

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "final_mark_display",
        "is_locked",
        "enrolled_at",
    )

    list_filter = ("course", "is_locked")

    actions = ["lock_enrollments"]

    def final_mark_display(self, obj):
        return obj.final_mark()

    final_mark_display.short_description = "Final Mark"

    def lock_enrollments(self, request, queryset):
        queryset.update(is_locked=True)

    lock_enrollments.short_description = "Lock selected enrollments"





from django.utils.timezone import now

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "final_mark_display",
        "status",
        "is_locked",
    )

    list_filter = ("course", "status", "is_locked")

    actions = [
        "submit_for_approval",
        "approve_enrollments",
        "lock_enrollments",
    ]

    def final_mark_display(self, obj):
        return obj.final_mark()

    final_mark_display.short_description = "Final Mark"

    # Lecturer action
    def submit_for_approval(self, request, queryset):
        queryset.filter(status="ACTIVE").update(status="SUBMITTED")

    submit_for_approval.short_description = "Submit grades for approval"

    # HOD action
    def approve_enrollments(self, request, queryset):
        queryset.filter(status="SUBMITTED").update(
            status="APPROVED",
            approved_by=request.user,
            approved_at=now()
        )

    approve_enrollments.short_description = "Approve grades"

    # Registrar action
    def lock_enrollments(self, request, queryset):
        queryset.filter(status="APPROVED").update(
            is_locked=True,
            status="COMPLETED"
        )

    lock_enrollments.short_description = "Lock approved enrollments"


'''

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "final_mark_display",
        "status",
    )

    actions = ["submit_grades"]

    def final_mark_display(self, obj):
        return obj.final_mark()

    final_mark_display.short_description = "Final Mark"

    def submit_grades(self, request, queryset):
        if request.user.role != "LECTURER":
            self.message_user(
                request,
                "Only lecturers can submit grades.",
                level="error"
            )
            return

        queryset.filter(status="ACTIVE").update(status="SUBMITTED")
