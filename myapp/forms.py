from django import forms
from .models import *
from django.core.exceptions import ValidationError


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    name=forms.CharField()
    place=forms.CharField()
    
    class Meta:
        model = User
        fields = ['name', 'place', 'password']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            login_obj = Login.objects.create(email=user.name, password=self.cleaned_data['password'])
            user.login = login_obj
            user.save()
        return user
    
# Password Reset Request Form should be outside the RegistrationForm class
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'form-control'
    }))
    
# forms.py

class EmployeeForm(forms.ModelForm):
    email = forms.EmailField(label="Email", max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    first_name = forms.CharField(label="First Name", max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label="Last Name", max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    phone = forms.CharField(label="Phone", max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Login.objects.filter(email=email).exists():
            raise ValidationError("Email already exists. Please use a different email.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        return password

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("Phone number must be 10 digits.")
        return phone
