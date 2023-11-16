from django.urls import include, path

urlpatterns = [
    path('v1/', include('apps.support.api.v1.urls')),
]
