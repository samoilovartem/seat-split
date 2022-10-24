from django.contrib import admin
from django.urls import path, include

from accounts_team.views import AccountsApiList, AccountsApiUpdate, AccountsApiDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts_team.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/accounts/', AccountsApiList.as_view()),
    path('api/v1/accounts/<int:pk>/', AccountsApiUpdate.as_view()),
    path('api/v1/accounts/delete/<int:pk>/', AccountsApiDestroyView.as_view()),
]
