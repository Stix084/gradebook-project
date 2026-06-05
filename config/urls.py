from django.contrib import admin
from django.urls import path, include




from users.views import (
    role_redirect,
    student_dashboard,
    lecturer_dashboard,
    lecturer_course_summary,
    export_course_summary,
    class_log,
    enter_grades,
    submit_assignment,
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
    path("lecturer/course/<int:id>/log/", class_log, name="class_log"),
    path("lecturer/course/<int:course_id>/assessment/<int:assessment_id>/grades/", enter_grades, name="enter_grades"),
    path("assessment/<int:assessment_id>/submit/", submit_assignment, name="submit_assignment"),
]