from rest_framework.exceptions import ValidationError


def validate_seat_range(value: str) -> str:
    """
    validate_seat_range function validates the 'seat' field.

    The function does the following validations:
    - If the seat is a range (i.e., contains '-'), it splits into first_seat and last_seat,
      and validates that both are positive integers, first_seat is less than last_seat,
      and first_seat is not equal to last_seat.
    - If the seat is not a range (i.e., a single seat), it validates that it is a positive integer.

    If any of the above validation fails, the function raises a validation error with an appropriate error message.
    If all validations pass, the function returns the seat value as is.

    Args:
        value (str): The 'seat' field value to validate.

    Returns:
        str: The 'seat' field value if all validations pass.

    Raises:
        ValidationError: Raised with an appropriate error message if any validation fails.
    """
    error_message = (
        'Invalid seat number. Seat(s) should be a positive integer or a range of positive integers.'
    )

    if '-' in value:
        try:
            first_seat, last_seat = map(int, value.split('-'))
            if first_seat <= 0 or last_seat <= 0:
                raise ValidationError(error_message)
            if first_seat > last_seat:
                raise ValidationError('First seat can not be higher than last seat.')
            if first_seat == last_seat:
                raise ValidationError(
                    'Single seat should not be in range format. Use a single seat number instead.'
                )
        except ValueError:
            raise ValidationError(error_message)

    else:
        try:
            if int(value) <= 0:
                raise ValidationError(error_message)
        except ValueError:
            raise ValidationError(error_message)

    return value
