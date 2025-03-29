from django.db import models

from chat.models import BaseModel, User

class UserStatistic(BaseModel):
    total_cases_opened = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')

class Item(BaseModel):
    pass
