from django.urls import path
from .views import enter_grades

urlpatterns = [
    path(
        "courses/<int:course_id>/grades/",
        enter_grades,
        name="enter_grades"
    ),
]
