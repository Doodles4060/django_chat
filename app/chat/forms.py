from django import forms
from django.core.validators import FileExtensionValidator

from .models import PFP
from .validators import validate_image_file_size


class RegistrationForm(forms.Form):
    username = forms.CharField(label='username', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=64)


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=64)


class PFPForm(forms.ModelForm):
    image = forms.ImageField(
        validators=[validate_image_file_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PFP
        fields = ['image']
