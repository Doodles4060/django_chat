from http.client import responses

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from chat.models import User, ChatGroup

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.test_user_username = 'testuser'
        self.test_user_password = 'testpassword'

        User.objects.create_user(
            username=self.test_user_username,
            password=self.test_user_password
        )

    def test_login_page_200(self):
        response = self.client.get(reverse('chat:login'))

        self.assertEqual(response.status_code, 200)

    def test_user_authentication_success(self):
        data = {
            'username': self.test_user_username,
            'password': self.test_user_password
        }
        response = self.client.post(reverse('chat:login'), data=data)
        user = response.wsgi_request.user

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], reverse('chat:user_profile_self'))
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, self.test_user_username)

    def test_user_authentication_failed(self):
        data = {
            'username': self.test_user_username,
            'password': self.test_user_password[:-1]
        }
        response = self.client.post(reverse('chat:login'), data=data, follow=True)
        user = response.wsgi_request.user

        self.assertEqual(response.status_code, 200)
        self.assertIn(reverse('chat:login'), response.wsgi_request.build_absolute_uri())
        self.assertFalse(user.is_authenticated)


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.test_user_username = 'testuser'
        self.test_user_password = 'testpassword'

        User.objects.create_user(
            username=self.test_user_username,
            password=self.test_user_password
        )

    def test_get_user_by_pk(self):
        user = User.objects.get(username=self.test_user_username)
        response = self.client.get(reverse('chat:user_profile', args=[user.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['requested_user'].pk, user.pk)

    def test_get_user_by_username(self):
        user = User.objects.get(username=self.test_user_username)
        response = self.client.get(reverse('chat:user_profile', args=[user.username]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['requested_user'].username, user.username)

    def test_get_current_user_if_authenticated(self):
        self.client.login(
            username=self.test_user_username,
            password=self.test_user_password
        )

        response = self.client.get(reverse('chat:user_profile_self'))

        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username=self.test_user_username)
        self.assertEqual(response.context['requested_user'], user)

class GroupListViewTestCase(TestCase):
    def test_group_list_view_200(self):
        response = self.client.get(reverse('chat:chat_group_list'))

        self.assertEqual(response.status_code, 200)


class ChatGroupViewTestCase(TestCase):
    def setUp(self):
        self.test_user_username = 'testuser'
        self.test_user_password = 'testpassword'

        User.objects.create_user(
            username=self.test_user_username,
            password=self.test_user_password
        )

        ChatGroup.objects.create(
            name='test'
        )

    def test_user_is_redirected_to_login_page_if_not_authenticated(self):
        status_codes = (301, 302)

        response = self.client.get(reverse('chat:chat_group', args=[1]))

        self.assertTrue(response.status_code in status_codes)
        self.assertTrue('Location' in response.headers)

    def test_chat_page_200_if_user_is_authenticated(self):
        self.client.login(
            username=self.test_user_username,
            password=self.test_user_password
        )

        response = self.client.get(reverse('chat:chat_group', args=['test']))

        self.assertEqual(response.status_code, 200)


class ChangePFPViewTestCase(TestCase):
    def setUp(self):
        self.test_image_path = 'chat/tests/test_files/pfpform_small_test_image.jpg'

    def test_pfp_upload(self):
        with open(self.test_image_path, 'rb') as test_image:
            test_image = SimpleUploadedFile('test_image.jpg', test_image.read())
            data = {'image': test_image}
            response = self.client.post(reverse('chat:upload_pfp'), data=data, follow=True)

            self.assertEqual(response.status_code, 200)