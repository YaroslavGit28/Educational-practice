from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .health import health_check

urlpatterns = [
    path('api/health/', health_check, name='health'),
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('users/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('processing/', include('processing.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('reports/', include('magazin.reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)