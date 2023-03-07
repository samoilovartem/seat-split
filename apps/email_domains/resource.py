from import_export import resources

from apps.email_domains.models import EmailDomains


class EmailDomainsResource(resources.ModelResource):
    class Meta:
        model = EmailDomains
        widgets = {
            'expiration_date': {'format': '%Y-%m-%d'},
        }
