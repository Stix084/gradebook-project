from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from courses.models import Course, Assessment, Grade
from enrollments.models import Enrollment


# ---------------------------------
# ROLE REDIRECT
# ---------------------------------
def role_redirect(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "STUDENT":
        return redirect("dashboard")

    return redirect("lecturer_dashboard")


# ---------------------------------
# STUDENT DASHBOARD
# ---------------------------------
@login_required
def student_dashboard(request):

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related("course")

    return render(request, "student/dashboard.html", {
        "enrollments": enrollments
    })


# ---------------------------------
# COURSE DETAIL
# ---------------------------------
@login_required
def course_detail(request, id):

    course = get_object_or_404(Course, id=id)

    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()

    assessments = Assessment.objects.filter(
        course=course
    )

    grades = Grade.objects.filter(
        student=request.user,
        assessment__course=course
    ).select_related("assessment")

    total_marks = 0
    total_possible = 0

    for grade in grades:
        total_marks += grade.marks_obtained
        total_possible += grade.assessment.total_marks

    percentage = (
        (total_marks / total_possible) * 100
        if total_possible > 0 else 0
    )

    return render(request, "courses/course_detail.html", {
        "course": course,
        "enrollment": enrollment,
        "assessments": assessments,
        "grades": grades,
        "percentage": percentage
    })


# ---------------------------------
# LECTURER DASHBOARD
# ---------------------------------
@login_required
def lecturer_dashboard(request):

    courses = Course.objects.filter(
        lecturer=request.user
    )

    return render(request, "lecturer/dashboard.html", {
        "courses": courses
    })