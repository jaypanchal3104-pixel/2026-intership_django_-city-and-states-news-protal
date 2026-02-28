from django.shortcuts import render
from .decorators import role_required


# Admin Dashboard
@role_required(allowed_roles=["admin"])
def adminDashboardView(request):
    return render(request, "dashboard/admin_dashboard.html")


# Editor Dashboard
@role_required(allowed_roles=["editor"])
def editorDashboardView(request):
    return render(request, "dashboard/editor_dashboard.html")


# Reporter Dashboard
@role_required(allowed_roles=["reporter"])
def reporterDashboardView(request):
    return render(request, "dashboard/reporter_dashboard.html")


# User Dashboard
@role_required(allowed_roles=["user"])
def userDashboardView(request):
    return render(request, "dashboard/user_dashboard.html")


# =========================
# COMMON ACTION PAGE
# =========================

def actionPageView(request):
    return render(request, "dashboard/common/action_page.html")


# =========================
# LOGOUT VIEW
# =========================

def logoutView(request):
 logout(request)
 return redirect("login")


# =========================
# ROLE WISE DASHBOARD REDIRECT
# =========================

def dashboardRedirectView(request):

    if request.user.role == "admin":
        return redirect("adminDashboardView")

    elif request.user.role == "editor":
        return redirect("editorDashboardView")

    elif request.user.role == "reporter":
        return redirect("reporterDashboardView")

    elif request.user.role == "user":
        return redirect("userDashboardView")

    else:
        return redirect("login")