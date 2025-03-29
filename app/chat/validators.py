from django.core.exceptions import ValidationError

def validate_image_file_size(file):
    if file.size > 1024**2:
        raise ValidationError('Image file too large ( > 1mb )')