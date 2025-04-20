from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('', include("django.contrib.auth.urls")),
]
