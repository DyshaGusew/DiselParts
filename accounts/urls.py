from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('confirm/<uidb64>/<token>/', views.register_confirm, name='register_confirm'),
    path('', include("django.contrib.auth.urls")),
]
