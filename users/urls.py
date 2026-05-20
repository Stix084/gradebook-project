from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from users.views import student_dashboard, course_detail

from users.views import (
    course_detail,
    role_redirect,
    student_dashboard,
    lecturer_dashboard
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("django.contrib.auth.urls")),

    path("", role_redirect, name="home"),

    path("dashboard/", student_dashboard, name="dashboard"),
    

    path(
        "lecturer-dashboard/",
        lecturer_dashboard,
        name="lecturer_dashboard"
    ),
     path("course/<int:id>/", course_detail, name="course_detail"),

     
]