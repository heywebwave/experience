from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'country', 'phone_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and placeholders
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your Email Address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your Last Name'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Enter your Phone Number'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter your Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email
    
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Email Address'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Password'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'