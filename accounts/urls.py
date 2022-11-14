from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'accounts', AccountsViewSet)

urlpatterns = [
    path('api/v1/authentication/', include('rest_framework.urls')),
    # path('api/v1/accounts/', AccountsApiList.as_view()),
    # path('api/v1/accounts/<int:pk>/', AccountsApiRetrieveUpdateDestroyView.as_view()),
    path('api/v1/', include(router.urls)),
    path('api/v1/accounts/token-auth/', views.obtain_auth_token),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
