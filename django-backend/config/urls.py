from django.contrib import admin
from django.urls import include, path

from config.yasg import urlpatterns as swagger_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.urls')),
]

urlpatterns += swagger_urls
