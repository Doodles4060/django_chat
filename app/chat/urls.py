from django.urls import path

from . import views

app_name = 'chat'

AUTH_URLS = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.RegistrationView.as_view(), name='signup'),
]

HOME_URLS = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('upload_pfp/', views.change_pfp, name='upload_pfp'),
]

CHAT_URLS = [
    path('groups/<int:pk>/', views.ChatGroupView.as_view(), name='chat_group'),
    path('groups/<str:group_name>/', views.ChatGroupView.as_view(), name='chat_group'),
]

urlpatterns = [
    path('lazy-bg-video/', views.lazy_background_video, name='lazy_bg_video'),
    *AUTH_URLS,
    *HOME_URLS,
    *CHAT_URLS,
]