from import_export import resources

from apps.accounts.models import Accounts


class AccountsResource(resources.ModelResource):
    class Meta:
        model = Accounts
        widgets = {
            'created_at': {'format': '%Y-%m-%d'},
            'last_opened': {'format': '%Y-%m-%d'},
        }
