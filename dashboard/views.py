from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .decorators import role_required


# ─────────────────────────────────────────────
#  ADMIN DASHBOARD
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def adminDashboardView(request):
    return render(request, "dashboard/admin_dashboard.html")


# ─────────────────────────────────────────────
#  JOURNALIST DASHBOARD
# ─────────────────────────────────────────────
@role_required(allowed_roles=["journalist"])
def journalistDashboardView(request):
    return render(request, "dashboard/journalist_dashboard.html")


# ─────────────────────────────────────────────
#  ADVERTISER DASHBOARD
# ─────────────────────────────────────────────
@role_required(allowed_roles=["advertiser"])
def advertiserDashboardView(request):
    return render(request, "dashboard/advertiser_dashboard.html")


# ─────────────────────────────────────────────
#  HOME  (user / reader role lands here)
# ─────────────────────────────────────────────
def homeView(request):
    return render(request, "core/home.html")


# ─────────────────────────────────────────────
#  UNAUTHORIZED PAGE
#  shown when a user tries to access a page
#  they don't have permission for
# ─────────────────────────────────────────────
def unauthorizedView(request):
    return render(request, "dashboard/unauthorized.html", status=403)


# ─────────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────────
def logoutView(request):
    logout(request)
    return redirect("login")


# ─────────────────────────────────────────────
#  ROLE-WISE DASHBOARD REDIRECT
# ─────────────────────────────────────────────
def dashboardRedirectView(request):
    if not request.user.is_authenticated:
        return redirect("login")

    role = request.user.role

    if role == "admin":
        return redirect("admin_dashboard")
    elif role == "journalist":
        return redirect("journalist_dashboard")
    elif role == "advertiser":
        return redirect("advertiser_dashboard")
    else:
        return redirect("home")