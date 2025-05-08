from django import template
from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import CustomLoginView

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('confirm/<uidb64>/<token>/', views.register_confirm, name='register_confirm'),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
            success_url=reverse_lazy('accounts:password_change_done'),
        ),
        name='password_change',
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ),
        name='password_change_done',
    ),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('', include("django.contrib.auth.urls")),
]
