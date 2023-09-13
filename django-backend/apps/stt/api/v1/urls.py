from djoser.views import TokenDestroyView

from django.urls import include, path

from apps.email_domains.api.v1.email_domains import (
    generate_random_data_with_provided_domain_or_state,
)
from apps.routers import main_router
from apps.stt.api.v1.login import CustomTokenCreateView
from apps.stt.api.v1.registration import RegisterView, VerifyView

urlpatterns = [
    path(
        'email-domains/generate_random_data_with_provided_domain_or_state/',
        generate_random_data_with_provided_domain_or_state,
    ),
    path('token-auth/token/login', CustomTokenCreateView.as_view(), name='login'),
    path('token-auth/token/logout', TokenDestroyView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:uidb64>/<str:token>/', VerifyView.as_view(), name='verify'),
    path('', include(main_router.urls)),
]
