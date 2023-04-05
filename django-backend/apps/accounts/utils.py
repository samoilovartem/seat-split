from tablib import Dataset, UnsupportedFormat

from apps.accounts.models import Accounts


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


def load_dataset_from_file(file):
    if file.name.endswith('.xlsx'):
        dataset = Dataset().load(file.read(), format='xlsx')
    elif file.name.endswith('.csv'):
        dataset = Dataset().load(file.read().decode('utf-8'), format='csv')
    else:
        raise UnsupportedFormat('Unsupported file format.')
    return dataset
