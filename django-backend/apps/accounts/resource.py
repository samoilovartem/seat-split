from apps.accounts.models import Accounts
from django.core.exceptions import ValidationError
from import_export import resources


class AccountsResource(resources.ModelResource):
    def before_save_instance(self, instance, using_transactions, dry_run):
        try:
            instance.full_clean()
        except ValidationError as e:
            raise e
        super(AccountsResource, self).before_save_instance(
            instance, using_transactions, dry_run
        )

    class Meta:
        model = Accounts
        widgets = {
            'created_at': {'format': '%Y-%m-%d'},
            'last_opened': {'format': '%Y-%m-%d'},
        }
