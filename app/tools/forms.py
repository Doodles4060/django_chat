from django import forms
from django.core.validators import FileExtensionValidator

from .validators import validate_svg

class SVGPixelationForm(forms.Form):
    svg_file = forms.FileField(label='SVG file to process',
                               validators=[validate_svg, FileExtensionValidator(allowed_extensions=['svg'])],
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    aspect_ratio = forms.CharField(label='Aspect ratio', max_length=32,
                                   widget=forms.TextInput(attrs={'placeholder': 'e.g. 16:9 or 16/9', 'class': 'form-control'}))
    pixelation_level = forms.IntegerField(label='Pixelation level', min_value=1, max_value=1000,
                                          widget=forms.TextInput(attrs={'class': 'form-control'}))
