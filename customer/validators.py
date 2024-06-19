from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_email_custom(value):
    if len(value) > 254:
        raise ValidationError(_("Email address must not exceed 254 characters."))

    if value.startswith('.') or value.startswith('@'):
        raise ValidationError(_("Email address must not start with a dot or @."))

    if '..' in value:
        raise ValidationError(_("Email address must not contain consecutive dots."))

    if value.count('@') != 1:
        raise ValidationError(_("Email address must contain exactly one @ symbol."))

    # Regex to check for illegal characters
    if re.search(r'[^\w.@+-]', value):
        raise ValidationError(_("Email address contains invalid characters."))

    return value