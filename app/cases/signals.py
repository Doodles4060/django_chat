from django.db.models.signals import post_save
from django.dispatch import receiver

from chat.models import User
from .models import UserStatistic

@receiver(post_save, sender=User)
def create_user_statistic(sender, instance, created, **kwargs):
    if created:
        UserStatistic.objects.create(user=instance)

