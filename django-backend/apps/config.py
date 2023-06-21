from pydantic import BaseSettings, Field


class AccountsCSVConfig(BaseSettings):
    duplicate_check_column: str = Field(
        default='email',
        description='The column to check for duplicates when importing from a CSV file.',
    )
    exclude_fields: list = Field(
        default=['updated_at', 'id'],
        description='The fields to exclude when importing from or exporting to a CSV file.',
    )
    strict_fields: list = Field(
        default=['recovery_email'],
        description='The fields that must be strictly presented in input CSV file.',
    )


class USAddressesCSVConfig(BaseSettings):
    exclude_fields: list = Field(
        default=['updated_at', 'created_at', 'id', 'location', 'is_used'],
        description='The fields to exclude when importing from a CSV file.',
    )


class VenuesCSVConfig(BaseSettings):
    exclude_fields: list = Field(
        default=['updated_at', 'created_at', 'id', 'latitude', 'longitude'],
        description='The fields to exclude when importing from a CSV file.',
    )
