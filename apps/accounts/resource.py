from import_export import resources
from import_export.fields import Field

from apps.accounts.models import Accounts


class AccountsResource(resources.ModelResource):
    class Meta:
        model = Accounts
        widgets = {
            'created_at': {'format': '%Y-%m-%d'},
            'last_opened': {'format': '%Y-%m-%d'},
        }


class ImportAccountsResource(resources.ModelResource):
    # Define the fields to be imported
    field1 = Field(attribute='field1', column_name='Field 1')
    field2 = Field(attribute='field2', column_name='Field 2')
    field3 = Field(attribute='field3', column_name='Field 3')

    class Meta:
        model = Accounts
