from django.forms import ModelForm
from .models import User
from django import forms

class LoginForm(ModelForm):
	class Meta:
		model=User
		fields=['email','password']
		widgets={
			'password':forms.PasswordInput(),
			'email':forms.TextInput(attrs={'required':True})
		}
