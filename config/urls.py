from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    # If user is logged in, go to dashboard, otherwise go to login
    if request.user.is_authenticated:
        return redirect('dashboard')  # or whatever your dashboard URL is named
    return redirect('login')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    
    # Homepage that redirects appropriately
    path("", home_redirect, name="home"),
    
    path("courses/", include("courses.urls")),
    path("users/", include("users.urls")),
    path("enrollments/", include("enrollments.urls")),
]