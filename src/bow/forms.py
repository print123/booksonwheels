from django.forms import ModelForm
from .models import User
from django import forms


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'required': True}),
            'email': forms.TextInput(attrs={'required': True}),
        }

class SignUpForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'required':True}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'required':True}))
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'required': True}),
            'email': forms.TextInput(attrs={'required': True}),
            'name': forms.TextInput(attrs={'required': True}),
            #'confirm_password':forms.PasswordInput(attrs={'required':True}),
        }

    def clean_confirm_password(self):
        print "hey bro whatsup man"
        if self.cleaned_data['password'] != self.cleaned_data['confirm_passworda']:
            raise forms.ValidationError("Pswd dnt match")


