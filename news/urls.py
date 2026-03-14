from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.newsListView,    name='news_list'),
    path('<int:pk>/',         views.newsDetailView,  name='news_detail'),
    path('create/',           views.newsCreateView,  name='news_create'),
    path('<int:pk>/edit/',    views.newsEditView,    name='news_edit'),
    path('<int:pk>/delete/',  views.newsDeleteView,  name='news_delete'),
    path('<int:pk>/approve/', views.newsApproveView, name='news_approve'),
    path('<int:pk>/reject/',  views.newsRejectView,  name='news_reject'),
    path('<int:pk>/comment/', views.addCommentView,  name='add_comment'), 
]