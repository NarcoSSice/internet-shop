from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from shop.services.auth_services import get_customer_activated


class RegisterCustomerForm(forms.Form):
    """
    Registration Form for creating users
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    phone = forms.CharField(required=True)

    def clean_phone(self):
        """ Function for validation phone """
        phone = self.cleaned_data.get('phone')
        if (phone[0] != '+') and (len(phone) != 13):
            raise ValidationError(
                _('Uncorrected phone number\nPhone number must consist:+380 ** *** ** **')
            )
        return phone

    def clean_password2(self):
        """ Function for validations passwords """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                _('password_mismatch')
            )
        return password2


class LoginUserForm(AuthenticationForm):
    """
    Login Form inherited from AuthenticationForm
    """

    def clean(self):
        """ add to method clean my function for validation input data """

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        get_customer_activated(self.request, email=username)

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
