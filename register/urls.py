from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from . import views
from django.urls import path, include

urlpatterns = [
    path('registration/', views.registration, name='registration'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html'),
         name='password_change'),
    path('password_change/done/', lambda r: redirect('profile'),
         name='password_change_done'),

    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile-update'),
]