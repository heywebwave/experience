from django import forms
from .models import CustomUser

class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name' ,'phone_number','country', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)