from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def role_redirect(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return redirect("dashboard")