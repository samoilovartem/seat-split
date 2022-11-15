from django.urls import path, include, re_path
from .routers import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.authtoken import views


urlpatterns = [
    path('api/v1/base-auth/', include('rest_framework.urls')),
    path('api/v1/', include(lawns_router.urls)),
    path('api/v1/', include(presales_router.urls)),
    path('api/v1/', include(mlb_router.urls)),
    path('api/v1/', include(nba_router.urls)),
    path('api/v1/', include(seasons_router.urls)),
    path('api/v1/', include(smallvenues_router.urls)),
    path('api/v1/', include(theatre_router.urls)),
    path('api/v1/', include(othersports_router.urls)),
    path('api/v1/', include(audrey_router.urls)),
    path('api/v1/accounts/token-auth/', views.obtain_auth_token),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
