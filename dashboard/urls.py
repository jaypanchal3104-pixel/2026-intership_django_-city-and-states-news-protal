from django.urls import path
from . import views

urlpatterns = [
    path("admin/", views.adminDashboardView, name="admin_dashboard"),
    path("editor/", views.editorDashboardView, name="editor_dashboard"),
    path("reporter/", views.reporterDashboardView, name="reporter_dashboard"),
    path("user/", views.userDashboardView, name="user_dashboard"),
    path("action/", views.actionPageView, name="actionPageView"),
    path("logout/", views.logoutView, name="logoutView"),
    path("dashboard-redirect/", views.dashboardRedirectView, name="dashboardRedirectView"),
    

]