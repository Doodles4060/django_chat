from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse_lazy
from time import sleep

from chat.models import User

class LoginPageLiveTestCase(LiveServerTestCase):
    def test_successful_user_login(self):
        test_user_username = 'testuser'
        test_user_password = 'testpassword'
        User.objects.create_user(
            username=test_user_username,
            password=test_user_password
        )

        driver = webdriver.Chrome()
        login_page = reverse_lazy('chat:login')

        driver.get(self.live_server_url + login_page)

        username = driver.find_element(By.NAME,'username')
        password = driver.find_element(By.NAME,'password')

        username.send_keys(test_user_username)
        password.send_keys(test_user_password)

        sleep(1)

        submit = driver.find_element(By.CSS_SELECTOR,'input[type="submit"][value="Submit"]')
        submit.send_keys(Keys.RETURN)

        self.assertIn(test_user_username, driver.page_source)