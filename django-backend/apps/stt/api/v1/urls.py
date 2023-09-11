from django.urls import path

from apps.email_domains.api.v1.email_domains import (
    generate_random_data_with_provided_domain_or_state,
)

urlpatterns = [
    path(
        'api/v1/email-domains/generate_random_data_with_provided_domain_or_state/',
        generate_random_data_with_provided_domain_or_state,
    ),
]
