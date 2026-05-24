from django.contrib import admin
from django.urls import path, include

from users.views import (
    role_redirect,
    student_dashboard,
    lecturer_dashboard,
    lecturer_course_summary,
    export_course_summary,
    course_detail
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", role_redirect, name="home"),
    path("dashboard/", student_dashboard, name="dashboard"),
    path("lecturer-dashboard/", lecturer_dashboard, name="lecturer_dashboard"),
    path("course/<int:id>/", course_detail, name="course_detail"),
    path("lecturer/course/<int:id>/", lecturer_course_summary, name="lecturer_course_summary"),
    path("lecturer/course/<int:id>/export/", export_course_summary, name="export_course_summary"),
]