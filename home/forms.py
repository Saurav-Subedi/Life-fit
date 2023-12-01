from .models import DeliveryAddress
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django import forms


class CustomerRegistrationForm(UserCreationForm):
    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'placeholder':'Email *'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'Username *'}))
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Password *'}))
    password2 = forms.CharField(label='Confirm Password(again)',
                                widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password *'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(
            attrs={})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True,'placeholder':'Username *'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password','placeholder':'Password *'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'autofocus': True}))

    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password'}), help_text=password_validation. password_validators_help_text_html())

    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(
        attrs={'autocomplete': 'email'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password'}), help_text=password_validation. password_validators_help_text_html())

    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password'}))



class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))

class CustomerVerificationForm(forms.Form):
    otp_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder': 'OTP code'}))

class SearchForm(forms.Form):
    query = forms.CharField(label='Search')

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['full_name', 'mobile_number', 'city', 'area', 'address', 'landmark']



class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')

class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(label='OTP Code')

class PasswordResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
