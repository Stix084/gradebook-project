from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from users.views import student_dashboard  # keep only this for now


def home_redirect(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return redirect("dashboard")


urlpatterns = [
    path("admin/", admin.site.urls),

    # auth system (Django built-in)
    path("accounts/", include("django.contrib.auth.urls")),

    # landing page
    path("", home_redirect, name="home"),

    # main student dashboard
    path("dashboard/", student_dashboard, name="dashboard"),
]