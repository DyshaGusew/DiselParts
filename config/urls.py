from django.contrib import admin
from django.urls import path, include
from love_page.views import LoveDariaView
from config.views import HomeView, AboutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("admin/", admin.site.urls),
    path("love-daria/", LoveDariaView.as_view(), name="love-daria"),
    path("catalog/", include(("catalog.urls", "catalog"), namespace="catalog")),
    path('about/', AboutView.as_view(), name='about'),
]
