from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse_lazy
from time import sleep

from chat.models import User
from .settings import WEB_DRIVER_CHROME

class LoginPageLiveTestCase(LiveServerTestCase):
    def test_successful_user_login(self):
        test_user_username = 'testuser'
        test_user_password = 'testpassword'
        User.objects.create_user(
            username=test_user_username,
            password=test_user_password
        )

        login_page = reverse_lazy('chat:login')

        WEB_DRIVER_CHROME.get(self.live_server_url + login_page)

        username = WEB_DRIVER_CHROME.find_element(By.NAME, 'username')
        password = WEB_DRIVER_CHROME.find_element(By.NAME, 'password')

        username.send_keys(test_user_username)
        password.send_keys(test_user_password)

        sleep(1)

        submit = WEB_DRIVER_CHROME.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Submit"]')
        submit.send_keys(Keys.RETURN)

        self.assertIn(test_user_username, WEB_DRIVER_CHROME.page_source)