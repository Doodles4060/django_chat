from django.urls import path

from . import views

app_name = 'chat'

LAZY_URLS = [
    path('lazy-bg-video/', views.lazy_background_video, name='lazy_bg_video'),
]

AUTH_URLS = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.RegistrationView.as_view(), name='signup'),
]

PROFILE_URLS = [
    path('users/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('users/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('users/', views.redirect_to_me, name='user_profile'),
    path('users/me', views.UserProfileView.as_view(), name='user_profile_self'),
]

HOME_URLS = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('upload_pfp/', views.change_pfp, name='upload_pfp'),
]

CHAT_URLS = [
    path('groups/', views.ChatGroupListView.as_view(), name='chat_group_list'),
    path('groups/<int:pk>/', views.ChatGroupView.as_view(), name='chat_group'),
    path('groups/<str:group_name>/', views.ChatGroupView.as_view(), name='chat_group'),
]

urlpatterns = [
    *LAZY_URLS,
    *AUTH_URLS,
    *HOME_URLS,
    *PROFILE_URLS,
    *CHAT_URLS,
]