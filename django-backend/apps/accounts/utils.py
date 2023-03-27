from apps.accounts.models import Accounts
from django.apps import apps
from django.db.models import Count
from tablib import Dataset, UnsupportedFormat


def accounts_per_value(filter_name):
    result = (
        Accounts.objects.values(filter_name)
        .order_by(filter_name)
        .annotate(count=Count(filter_name))
    )
    return result


def get_existing_emails(email_column, dataset):
    emails = [row[email_column] for row in dataset]
    existing_emails = Accounts.objects.filter(email__in=emails).values_list(
        'email', flat=True
    )
    error_messages = [
        f'Email {email} already exists in the database.' for email in existing_emails
    ]
    return error_messages


def get_validation_errors(email_column, invalid_rows):
    error_messages = []
    for invalid_row in invalid_rows:
        email = invalid_row.values[email_column + 1]
        error_messages.append(f'Errors in email {email}. Columns: {invalid_row.error}')
    return error_messages


def get_accounts_fields():
    Accounts = apps.get_model('accounts', 'Accounts')
    field_names = [field.name for field in Accounts._meta.fields]
    field_names.remove('id')
    field_names.remove('updated_at')
    return field_names


def load_dataset_from_file(file):
    if file.name.endswith('.xlsx'):
        dataset = Dataset().load(file.read(), format='xlsx')
    elif file.name.endswith('.csv'):
        dataset = Dataset().load(file.read().decode('utf-8'), format='csv')
    else:
        raise UnsupportedFormat('Unsupported file format.')
    return dataset


def get_dataset_to_export():
    queryset = Accounts.objects.all()
    if not queryset.exists():
        return None
    headers = ['email', 'first_name', 'last_name', 'created_at']
    rows = [
        [
            account.email,
            account.first_name,
            account.last_name,
            account.created_at.strftime('%Y-%m-%d'),
        ]
        for account in queryset
    ]
    return SimpleDataSource(headers=headers, data=rows)
