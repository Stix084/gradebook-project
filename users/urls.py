from django.contrib import admin
from django.urls import path, include


path(
    "lecturer/course/<int:course_id>/summary/",
    lecturer_course_summary,
    name="lecturer_course_summary"
),

from users.views import (
    lecturer_course_summary,
    role_redirect,
    student_dashboard,
    lecturer_dashboard,
    course_detail
)

from courses.views import enter_grades


urlpatterns = [
    path("admin/", admin.site.urls),

    # Django auth
    path("accounts/", include("django.contrib.auth.urls")),

    # Home redirect
    path("", role_redirect, name="home"),

    # Student dashboard
    path("dashboard/", student_dashboard, name="dashboard"),

    # Lecturer dashboard
    path("lecturer-dashboard/", lecturer_dashboard, name="lecturer_dashboard"),

    # Course detail (student view)
    path("course/<int:id>/", course_detail, name="course_detail"),

    # Lecturer grading
    path("lecturer/grades/<int:course_id>/", enter_grades, name="enter_grades"),
]