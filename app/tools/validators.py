from mimetypes import guess_type
from django.core.exceptions import ValidationError

def validate_svg(file):
    mime_type, _ = guess_type(file.name)
    if mime_type != "image/svg+xml":
        raise ValidationError("Only SVG files are allowed.")
