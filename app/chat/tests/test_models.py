from django.test import TestCase

from chat.models import User, PFP

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='testuser', password='testpassword')

    def test_user_creation(self):
        users = User.objects.all()
        self.assertEqual(len(users), 1)

class PFPTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="testpassword")

    def test_pfp_created_on_user_creation(self):
        user = User.objects.get(username="testuser")

        user_pfp = PFP.objects.filter(user=user).first()

        self.assertIsNotNone(user_pfp)
        self.assertEqual(user_pfp.user, user)
        self.assertEqual(user_pfp.image.name, 'default/user_default.png')  # Ensuring default image is set
