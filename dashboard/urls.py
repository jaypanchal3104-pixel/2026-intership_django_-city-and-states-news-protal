from django.urls import path
from . import views

urlpatterns = [

    # ── Dashboards ──
    path("admin/",        views.adminDashboardView,      name="admin_dashboard"),
    path("journalist/",   views.journalistDashboardView, name="journalist_dashboard"),
    path("advertiser/",   views.advertiserDashboardView, name="advertiser_dashboard"),
    path("home/",         views.homeView,                name="home"),
    path("redirect/",     views.dashboardRedirectView,   name="dashboard_redirect"),
    path("unauthorized/", views.unauthorizedView,        name="unauthorized"),
    path("logout/",       views.logoutView,              name="logout"),

    # ── AJAX API ──
    path("api/cities/",   views.citiesApiView,           name="api_cities"),

    # ── Admin — Content ──
    path("admin/pending/",                  views.pendingNewsView,      name="admin_pending"),

    # ── Admin — Categories ──
    path("admin/categories/",               views.categoriesView,       name="admin_categories"),
    path("admin/categories/<int:pk>/delete/", views.categoryDeleteView,  name="admin_category_delete"),

    # ── Admin — States ──
    path("admin/states/",                   views.statesView,           name="admin_states"),
    path("admin/states/<int:pk>/delete/",   views.stateDeleteView,      name="admin_state_delete"),

    # ── Admin — Cities ──
    path("admin/cities/",                   views.citiesView,           name="admin_cities"),
    path("admin/cities/<int:pk>/delete/",   views.cityDeleteView,       name="admin_city_delete"),

    # ── Admin — Users ──
    path("admin/journalists/",              views.journalistsView,      name="admin_journalists"),
    path("admin/readers/",                  views.readersView,          name="admin_readers"),
    path("admin/advertisers/",              views.advertisersView,      name="admin_advertisers"),

    # ── Admin — System ──
    path("admin/comments/",                 views.commentsView,         name="admin_comments"),
    path("admin/comments/<int:pk>/delete/", views.commentDeleteView,    name="admin_comment_delete"),
    path("admin/advertisements/",           views.advertisementsView,   name="admin_advertisements"),
    path("admin/analytics/",                views.analyticsView,        name="admin_analytics"),
]