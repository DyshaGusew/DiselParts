from django.contrib import admin
from django.urls import path, include
from love_page.views import LoveDariaView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("love-daria/", LoveDariaView.as_view(), name="love-daria"),
    path("catalog/", include("catalog.urls")),
]
