from django.contrib import admin
from django.urls import path, include
from love_page.views import LoveDariaView
from config.views import HomeView, AboutView, SertView
from .sitemaps import ProductSitemap, StaticSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

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
    path(
        'robots.txt',
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
