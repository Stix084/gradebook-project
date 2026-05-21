from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from courses.models import Course
from enrollments.models import Enrollment


# ----------------------------
# ROLE REDIRECT (SINGLE SOURCE)
# ----------------------------
def role_redirect(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "STUDENT":
        return redirect("dashboard")

    return redirect("lecturer_dashboard")


# ----------------------------
# COURSE DETAIL
# ----------------------------
@login_required
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()

    return render(request, "courses/course_detail.html", {
        "course": course,
        "enrollment": enrollment
    })


# ----------------------------
# STUDENT DASHBOARD
# ----------------------------
@login_required
def student_dashboard(request):
    enrollments = request.user.enrollment_set.all()

    return render(request, "student/dashboard.html", {
        "enrollments": enrollments
    })


# ----------------------------
# LECTURER DASHBOARD
# ----------------------------
@login_required
def lecturer_dashboard(request):
    return render(request, "lecturer/dashboard.html")