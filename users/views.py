from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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

