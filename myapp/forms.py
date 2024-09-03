from django import forms
from .models import Login, User

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