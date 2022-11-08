from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from accounts_team.views import AccountsApiList, AccountsApiUpdate, AccountsApiDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts_team.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/accounts/', AccountsApiList.as_view()),
    path('api/v1/accounts/<int:pk>/', AccountsApiUpdate.as_view()),
    path('api/v1/accounts/<int:pk>/delete/', AccountsApiDestroyView.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls')), ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
