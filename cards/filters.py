from django_filters import rest_framework as filters
from .models import Cards


class CardsFilterSet(filters.FilterSet):
    class Meta:
        model = Cards
        fields = {
            'id': ['exact', 'in', 'range'],
            'created_at': ['exact', 'in', 'range', 'startswith', 'contains'],
        }

        # @classmethod
        # def get_fields(cls):
        #     fields = super().get_fields()
        #     for field_name in fields.copy():
        #         lookup_list = cls.Meta.model._meta.get_field(field_name).get_lookups().keys()
        #         fields[field_name] = lookup_list
        #     return fields

    """
    'range' = field__range=<start>,<end> (range of objects)
    'in' = field__in=<object_1>,<object_2> etc (particular objects)
    'exact' = field=<value> (one object match)
    """
