from django.contrib import admin
from django.urls import path, include
from love_page.views import LoveDariaView
from config.views import HomeView, AboutView, SertView
from .sitemaps import ProductSitemap, StaticSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'products': ProductSitemap,
    'static': StaticSitemap,
}

admin.site.site_title = "Дизельпартс админпанель"
admin.site.site_header = "Панель администрирования ДИЗЕЛЬПАРТС"
admin.site.index_title = "Панель администрирования ДИЗЕЛЬПАРТС"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("admin/", admin.site.urls),
    path("love-daria/", LoveDariaView.as_view(), name="love-daria"),
    path("catalog/", include(("catalog.urls", "catalog"), namespace="catalog")),
    path('about/', AboutView.as_view(), name='about'),
    path('sert/', SertView.as_view(), name='sert'),
    path('accounts/', include('accounts.urls')),
    path("order/", include(("order.urls", "order"), namespace="order")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
