from django.forms import ModelForm
from .models import User
from django import forms


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'required': True}),
            'email': forms.TextInput(attrs={'required': True})
        }


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'required': True}),
            'email': forms.TextInput(attrs={'required': True}),
            'name': forms.TextInput(attrs={'required': True}),
        }
