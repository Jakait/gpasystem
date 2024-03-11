from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

import re

class UserRegistrationForm(UserCreationForm):
    USER_TYPES = [
        (1, 'Admin'),
        (3, 'Student'),
        (2, 'Lecturer'),
    ]

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}))
    firstname = forms.CharField(max_length=66, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(max_length=66, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last name'}))
    middle_name = forms.CharField(max_length=66, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Middle Name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    accesslevel = forms.ChoiceField(choices=USER_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ( 'email', 'phone_number', 'firstname','last_name','middle_name','password1','accesslevel')
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Remove any non-digit characters from the phone number
        cleaned_phone_number = re.sub(r'\D', '', phone_number)

        if len(cleaned_phone_number) < 10 or len(cleaned_phone_number) > 13:
            raise forms.ValidationError("Phone number must have between 10 and 13 digits")

        if not cleaned_phone_number.startswith(('+254', '254', '0')):
            raise forms.ValidationError("Phone number must start with +254, 254, or 0")

        return phone_number
