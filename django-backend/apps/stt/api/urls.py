from django.urls import include, path

urlpatterns = [
    path('v1/', include('apps.stt.api.v1.urls')),
]
