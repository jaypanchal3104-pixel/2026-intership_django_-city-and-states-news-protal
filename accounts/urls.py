from django.urls import path
from . import views

urlpatterns = [
    path('profile/',          views.profileView,        name='profile'),
    path('profile/edit/',     views.profileEditView,    name='profile_edit'),
    path('profile/password/', views.changePasswordView, name='change_password'),
    path('bookmarks/',        views.bookmarksView,      name='bookmarks'),
    path('bookmarks/<int:news_id>/toggle/', views.bookmarkToggleView, name='bookmark_toggle'),
    path('comments/',         views.myCommentsView,     name='my_comments'),
]