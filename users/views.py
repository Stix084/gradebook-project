from django.shortcuts import redirect


def role_redirect(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return redirect("dashboard")