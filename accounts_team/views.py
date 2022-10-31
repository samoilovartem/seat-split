import json

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

import pandas as pd
import gspread


def log_in(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'accounts_team/log_in.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('home')


class AccountsView(ListView):
    model = Accounts
    template_name = 'accounts_team/index.html'
    context_object_name = 'accounts'
    extra_context = {'title': 'Lew & Dowski'}
    paginate_by = 15
    # permission_required = ''


class UpdateAccounts(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Accounts
    form_class = AccountsForm
    template_name = 'accounts_team/update_account.html'
    context_object_name = 'update_account_item'
    success_url = reverse_lazy('home')
    login_url = '/login/'
    permission_required = ''
    # raise_exception = True


class AddAccount(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = AccountsForm
    template_name = 'accounts_team/add_account.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'
    permission_required = ''
    # raise_exception = True


class DeleteAccount(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Accounts
    template_name = 'accounts_team/delete_account.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'
    permission_required = ''
    context_object_name = 'delete_account_item'


def index(request):
    accounts = get_data()
    json_records = accounts.reset_index().to_json(orient='records')
    data = json.loads(json_records)
    context = {'data': data, 'title': 'All accounts'}
    return render(request, 'accounts_team/gsheet_version.html', context)


def get_data():
    gp = gspread.service_account(filename='/Users/samoylovartem/Projects/Lew&Dowski '
                                          'projects/accounts_team_django_project/mysite/Gservice.json')

    google_sheet = gp.open_by_url(
        'https://docs.google.com/spreadsheets/d/1eKdNvXwWvGMADmglb2tyR9XOGbcE13Q-Ttf_aX270hU/')

    trade_shift_dict = google_sheet.worksheet('Amex Tradeshift').get_all_records()
    citi_virtual_dict = google_sheet.worksheet('Citi Virtual').get_all_records()
    global_rewards_dict = google_sheet.worksheet('Global Rewards').get_all_records()
    divvy_visa_dict = google_sheet.worksheet('Divvy Visa').get_all_records()

    data_frame_trade_shift = pd.DataFrame(trade_shift_dict)
    data_frame_citi_virtual = pd.DataFrame(citi_virtual_dict)
    data_frame_global_rewards = pd.DataFrame(global_rewards_dict)
    data_frame_divvy_visa = pd.DataFrame(divvy_visa_dict)

    final_data_frame = pd.concat([
        data_frame_trade_shift,
        data_frame_citi_virtual,
        data_frame_global_rewards,
        data_frame_divvy_visa
    ], ignore_index=True)
    return final_data_frame


class AccountsApiList(ListCreateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
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






