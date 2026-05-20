from django.contrib import admin
from django.urls import path, include
from users.views import (
    role_redirect,
    student_dashboard,
    lecturer_dashboard,
    course_detail
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("django.contrib.auth.urls")),

    path("", role_redirect, name="home"),

    path("dashboard/", student_dashboard, name="dashboard"),

    path("lecturer-dashboard/", lecturer_dashboard, name="lecturer_dashboard"),

    path("course/<int:id>/", course_detail, name="course_detail"),
]