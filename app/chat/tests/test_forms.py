from io import BytesIO

from PIL import Image
from chat.forms import PFPForm
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class PFPFormTestCase(TestCase):
    def setUp(self):
        self.small_test_image_path = 'chat/tests/test_files/pfpform_small_test_image.jpg'
        self.large_test_image_path = 'chat/tests/test_files/pfpform_large_test_image.png'

    def test_valid_pfp_upload(self):
        with open(self.small_test_image_path, 'rb') as test_file:
            image = SimpleUploadedFile('test.png', test_file.read())

            form = PFPForm(data={}, files={"image": image})
            self.assertTrue(form.is_valid())

    def test_max_image_size_validation(self):
        with open(self.large_test_image_path, 'rb') as test_file:
            image = SimpleUploadedFile('test.png', test_file.read())

            form = PFPForm(data={}, files={"image": image})
            self.assertFalse(form.is_valid())
