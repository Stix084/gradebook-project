from django.core.exceptions import PermissionDenied

def lecturer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        if request.user.role != "LECTURER":
            raise PermissionDenied

        return view_func(request, *args, **kwargs)
    return wrapper
