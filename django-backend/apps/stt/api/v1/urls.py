from django.urls import path

from apps.email_domains.api.v1.email_domains import (
    generate_random_data_with_provided_domain_or_state,
)
from apps.stt.api.v1.authentication import (
    CustomTokenCreateView,
    TokenDestroyView,
)
from apps.stt.api.v1.registration import RegisterView, VerifyView
from apps.stt.api.v1.timezones import TimezoneListView

urlpatterns = [
    path(
        'email-domains/generate_random_data_with_provided_domain_or_state/',
        generate_random_data_with_provided_domain_or_state,
    ),
    path('token-auth/token/login/', CustomTokenCreateView.as_view(), name='login'),
    path('token-auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<str:uidb64>/<str:token>/', VerifyView.as_view(), name='verify'),
    path('timezones/', TimezoneListView.as_view(), name='timezones'),
]
