# users/urls.py
from django.urls import path
from django.http import HttpResponse

# Simple inline view for testing
def test_view(request):
    return HttpResponse("Test view working!")

urlpatterns = [
    path('', test_view, name='home'),
]