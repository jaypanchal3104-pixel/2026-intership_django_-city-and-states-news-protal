from django.shortcuts import render

# Create your views here.

def adminDashboardView(request):
    return render(request, "dashboard/admin_dashboard.html")

def editorDashboardView(request):
    return render(request, "dashboard/editor_dashboard.html")

def reporterDashboardView(request):
    return render(request, "dashboard/reporter_dashboard.html")

def userDashboardView(request):
    return render(request, "dashboard/user_dashboard.html")