from django.urls import path, include, re_path

from patches.routers import main_router

urlpatterns = [
    path('api/v1/base-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('api/v1/', include(main_router.urls))
]
