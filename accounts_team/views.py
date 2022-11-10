from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAdminOrReadOnly
from .serializers import AccountsSerializer
from .pagination import AccountsApiListPagination

from .models import Accounts

from .forms import AccountsForm, UserLoginForm
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from django_tables2 import SingleTableView, LazyPaginator
from django_filters.views import FilterView

from .tables import AccountsTable
from .filters import AccountFilter


def log_in(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('home')


class AccountsView(ListView):
    model = Accounts
    # template_name = 'accounts_team/index.html'
    template_name = 'accounts_team/index_table.html'
    context_object_name = 'accounts'
    # The wat we can get model field names:
    # field_names = [f.name for f in Accounts._meta.get_fields()]
    extra_context = {
        'title': 'Lew & Dowski',
        # 'field_names': field_names
    }
    paginate_by = 15
    # permission_required = ''


class UpdateAccounts(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Accounts
    form_class = AccountsForm
    template_name = 'accounts_team/update_account.html'
    context_object_name = 'update_account_item'
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'
    permission_required = ''
    # raise_exception = True


class AddAccount(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = AccountsForm
    template_name = 'accounts_team/add_account.html'
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'
    permission_required = ''
    # raise_exception = True


class DeleteAccount(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Accounts
    template_name = 'accounts_team/delete_account.html'
    success_url = reverse_lazy('home')
    login_url = '/accounts/login/'
    permission_required = ''
    context_object_name = 'delete_account_item'


class AccountsApiList(ListCreateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = AccountsApiListPagination


class AccountsApiUpdate(RetrieveUpdateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication, )


class AccountsApiDestroyView(RetrieveDestroyAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AccountsTableView(SingleTableView, FilterView):
    table_class = AccountsTable
    queryset = Accounts.objects.all()
    paginate_by = 5
    # paginator_class = LazyPaginator
    filterset_class = AccountFilter
    template_name = "accounts_team/index_table.html"




