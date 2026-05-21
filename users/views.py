from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from django.shortcuts import render, get_object_or_404
from enrollments.models import Enrollment


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



def role_redirect(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "LECTURER":
        return redirect("lecturer_dashboard")

    return redirect("dashboard")


@login_required
def student_dashboard(request):

    enrollments = request.user.enrollment_set.all()

    return render(request, "student/dashboard.html", {
        "enrollments": enrollments
    })



@login_required
def lecturer_dashboard(request):

    return render(request, "lecturer/dashboard.html")

