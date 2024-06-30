from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class PasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        users = CustomUser.objects.filter(email=email)
        if users.exists():
            if users.first().is_active:
                return email
            else:
                raise ValidationError("The provided email is not activated.")
        else:
            raise ValidationError("The provided email is not registered.")
