from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect

def role_redirect(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "STUDENT":
        return redirect("student_dashboard")

    if request.user.role == "LECTURER":
        return redirect("lecturer_dashboard")

    return redirect("admin:index")