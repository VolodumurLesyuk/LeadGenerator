from django import forms

from customer.validators import validate_email_custom


from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class EmailCheckForm(forms.Form):
    email = forms.EmailField(max_length=35)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address")
        return email


