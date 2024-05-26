import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

phone_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="The phone number is wrong. The phone number must be 11 digits and start with 09",
)


def national_id_validator(input: str):
    if not re.search(r"^\d{10}$", input):
        raise ValidationError("National ID must have 10 digits!")
    control_digit = int(input[9])
    s = sum(int(input[i]) * (10 - i) for i in range(9)) % 11
    if s < 2:
        if control_digit != s:
            raise ValidationError("Invalid National ID!")
    elif control_digit + s != 11:
        raise ValidationError("Invalid National ID!")
