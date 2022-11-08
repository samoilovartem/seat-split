from django.urls import path
from .views import *

urlpatterns = [
    path('', AccountsView.as_view(), name='home'),
    # path('', AccountsTableView.as_view(), name='home'),
    path('<int:pk>/edit/', UpdateAccounts.as_view(), name='update_account'),
    path('add-account/', AddAccount.as_view(), name='add_account'),
    path('<int:pk>/delete/', DeleteAccount.as_view(), name='delete_account'),
]
