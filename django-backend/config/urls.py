from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from config.settings import MEDIA_ROOT
from config.yasg import urlpatterns as swagger_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.urls')),
]

urlpatterns += swagger_urls + [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})
]
