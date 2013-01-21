# Copyright 2013 Hansel Dunlop
# All rights reserved
#
# Author: Hansel Dunlop - hansel@interpretthis.org
#

from django import forms
from django.contrib.auth.models import User

ERRORS = {
        'duplicate_username': 'Sorry, that username is already taken',
        'passwords_differ': 'Passwords do not match'
}

class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'tabindex': '1',
                'autocorrect': 'off',
                'autocapitalize': 'off',
            },
        ),
        max_length=64,
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email address',
                'tabindex': '2',
                'autocorrect': 'off',
                'autocapitalize': 'off',
            },
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'tabindex': '3',
            },
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password',
                'tabindex': '4',
            },
        )
    )

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if User.objects.filter(
            username=cleaned_data.get('username')
        ).exists():
            raise forms.ValidationError(ERRORS['duplicate_username'])

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(ERRORS['passwords_differ'])

        return cleaned_data


