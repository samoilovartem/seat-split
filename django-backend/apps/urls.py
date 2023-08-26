from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import include, path

from apps.common_services.jwt_token_claims import CustomTokenObtainPairView
from apps.email_domains.api.v1.email_domains import (
    generate_random_data_with_provided_domain_or_state,
)
from apps.routers import main_router
from apps.stt.api.v1.auth import RegisterView
from apps.stt.api.v1.teams import TeamsAndLeaguesInfoView

urlpatterns = [
    path('api/v1/base-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path(
        'api/v1/auth/jwt/login/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path('api/v1/auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/', include(main_router.urls)),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path(
        'api/v1/teams-and-leagues-info/',
        TeamsAndLeaguesInfoView.as_view(),
        name='teams-and-leagues-info',
    ),
    path(
        'api/v1/email-domains/generate_random_data_with_provided_domain_or_state/',
        generate_random_data_with_provided_domain_or_state,
    ),
]
