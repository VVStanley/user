from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class AuthenticationForm(AuthenticationForm):

    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Почта или телефон'
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': 'form-control',
                'placeholder': 'Пароль'
            }
        ),
    )


class PasswordForm(forms.Form):

    password = forms.CharField(
        label=_("enter the received code"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Пароль'
            }
        ),
    )


class RegistrationForm(forms.Form):

    email_or_phone = forms.CharField(
        label=_('email or phone'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Почта или телефон'
            }
        ),
        required=True,
    )


class AddBalance(forms.Form):

    balance = forms.DecimalField(
        label=_('balance'),
        required=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Сумма'
            }
        )
    )
