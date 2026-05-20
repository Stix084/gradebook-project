# users/urls.py
from django.urls import path
from django.http import HttpResponse
from . import views  # Import your views

# Simple inline view for testing
def test_view(request):
    return HttpResponse("Test view working!")

urlpatterns = [
    path('', test_view, name='home'),
    # Add dashboard URLs
    path('lecturer-dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

