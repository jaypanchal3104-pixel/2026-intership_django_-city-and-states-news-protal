from django.shortcuts import redirect, HttpResponse
from functools import wraps


def role_required(allowed_roles=None):

    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):

        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):

            # Login check
            if not request.user.is_authenticated:
                return redirect("login")

            # Role check
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # Unauthorized
            return HttpResponse("You are not authorized to view this page")

        return wrapper_func

    return decorator