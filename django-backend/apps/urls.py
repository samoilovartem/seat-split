from djoser.views import TokenDestroyView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import include, path

from apps.routers import main_router
from apps.stt.api.v1.login import CustomTokenCreateView, CustomTokenObtainPairView
from apps.stt.api.v1.registration import RegisterView, VerifyView

urlpatterns = [
    path('api/v1/base-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path(
        'api/v1/token-auth/token/login', CustomTokenCreateView.as_view(), name='login'
    ),
    path('api/v1/token-auth/token/logout', TokenDestroyView.as_view(), name='logout'),
    path(
        'api/v1/auth/jwt/create/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path('api/v1/auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/', include('apps.stt.api.v1.urls')),
    path('api/v1/', include(main_router.urls)),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path(
        'api/v1/verify/<str:uidb64>/<str:token>/', VerifyView.as_view(), name='verify'
    ),
]
