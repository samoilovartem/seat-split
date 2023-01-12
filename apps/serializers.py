class ConvertNoneToStringSerializerMixin:

    def get_none_to_str_fields(self):
        meta = getattr(self, 'Meta', None)
        return getattr(meta, 'none_to_str_fields', [])

    def to_representation(self, instance):
        fields = self.get_none_to_str_fields()
        data = super().to_representation(instance)

        if not fields or not isinstance(data, dict):
            return data

        for field in fields:
            if field in data and data[field] is None:
                data[field] = 'NA'
        return data
