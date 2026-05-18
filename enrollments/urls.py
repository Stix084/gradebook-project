from django.urls import path
from .views import student_grades

urlpatterns = [
    path("my-grades/", student_grades, name="student_grades"),
]
