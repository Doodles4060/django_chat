from django.urls import path

from . import views

app_name = 'cases'

USER_STATS_URLS = [
    path('users/stats/', views.UserStatisticsView.as_view(), name='user_statistics'),
    path('users/<int:pk>/stats/', views.UserStatisticsView.as_view(), name='user_statistics'),
    path('users/<str:username>/stats/', views.UserStatisticsView.as_view(), name='user_statistics'),
]

urlpatterns = [
    *USER_STATS_URLS,
]
