from django.contrib import admin
from django.urls import path, include
from users.views import role_redirect

urlpatterns = [
    path("admin/", admin.site.urls),

    # authentication
    path("accounts/", include("django.contrib.auth.urls")),

    # landing redirect
    path("", role_redirect, name="home"),

    # app modules
    path("courses/", include("courses.urls")),
    path("enrollments/", include("enrollments.urls")),
    path("users/", include("users.urls")),
]