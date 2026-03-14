from django.urls import path
from . import views

urlpatterns = [
    path("admin/",      views.adminDashboardView,      name="admin_dashboard"),
    path("journalist/", views.journalistDashboardView, name="journalist_dashboard"),
    path("advertiser/", views.advertiserDashboardView, name="advertiser_dashboard"),
    path("home/",       views.homeView,                name="home"),
    path("logout/",     views.logoutView,              name="logout"),
    path("redirect/",   views.dashboardRedirectView,   name="dashboard_redirect"),
    path("unauthorized/", views.unauthorizedView,        name="unauthorized"),
     path("api/cities/",   views.citiesApiView,           name="api_cities"),
]