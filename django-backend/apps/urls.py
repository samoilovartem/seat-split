from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import include, path

from apps.routers import main_router
from apps.stt.api.v1.authentication import CustomTokenObtainPairView

urlpatterns = [
    path('api/v1/base-auth/', include('rest_framework.urls')),
    path('api/', include('apps.stt.api.urls')),
    path('api/', include('apps.support.api.urls')),
    path(
        'api/v1/auth/jwt/create/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path('api/v1/auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/', include(main_router.urls)),
]
