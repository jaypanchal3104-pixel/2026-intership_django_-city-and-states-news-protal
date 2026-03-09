from django.shortcuts import redirect
from functools import wraps


def role_required(allowed_roles=None):

    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):

        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):

            # ── Not logged in → login page ──
            if not request.user.is_authenticated:
                return redirect("login")

            # ── Correct role → allow access ──
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # ── Wrong role → unauthorized page ──
            return redirect("unauthorized")

        return wrapper_func

    return decorator