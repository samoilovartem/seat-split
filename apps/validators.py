from django.core.exceptions import ValidationError


def any_or_na(field):
    if not field or len(field) < 2:
        raise ValidationError("If this field is not applicable to you, "
                              "please input NA")
    if len(field) == 2 and field != 'NA':
        raise ValidationError("If this field is not applicable to you, "
                              "please input NA")
    if field == 'N/A':
        raise ValidationError("If this field is not applicable to you, "
                              "please input NA")
    return field
