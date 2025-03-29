from django.test import TestCase
from django.shortcuts import get_object_or_404

from chat.models import User
from cases.models import UserStatistic

class UserStatisticTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="testpassword")

    def test_statistic_created_on_user_creation(self):
        user = User.objects.get(username="testuser")

        user_stats = UserStatistic.objects.filter(user=user).first()

        self.assertIsNotNone(user_stats)
        self.assertEqual(user_stats.user, user)
        self.assertEqual(user_stats.total_cases_opened, 0)  # Ensuring default image is set