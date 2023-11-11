from django.urls import include, path

from apps.stt.api.health_check import health_check

urlpatterns = [
    path('v1/', include('apps.stt.api.v1.urls')),
    path('health-check/', health_check, name='health-check'),
]
