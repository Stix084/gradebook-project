from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def role_redirect(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "LECTURER":
        return redirect("lecturer_dashboard")

    return redirect("dashboard")

