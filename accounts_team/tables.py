import django_tables2 as tables
from django_tables2 import A

from .models import Accounts


class AccountsTable(tables.Table):
    edit = tables.LinkColumn('update_account',
                             text='Edit',
                             args=[A('pk')],
                             orderable=False,
                             empty_values=())

    class Meta:
        model = Accounts
        exclude = ('created_at', 'updated_at')
