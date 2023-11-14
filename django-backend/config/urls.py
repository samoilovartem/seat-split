from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.settings import MEDIA_ROOT, MEDIA_URL
from config.yasg import urlpatterns as swagger_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.urls')),
]

urlpatterns += swagger_urls + static(MEDIA_URL, document_root=MEDIA_ROOT)
