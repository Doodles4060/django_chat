from io import BytesIO

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models

from typing import Union

BaseModel = models.Model

class User(AbstractUser):
    pass

class PFP(BaseModel):
    image = models.ImageField(upload_to='profile_pics/', default='default/user_default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pfp')

    def save(self, *args, **kwargs):
        if self.image and 'user_default.png' not in self.image.name:
            img = Image.open(self.image)

            img_format = img.format
            img = img.resize((512, 512))

            buf = BytesIO()
            img.save(buf, format=img_format, quality=90)

            file_name = '{}_profile.jpg'.format(self.user.username)

            self.image.save(file_name, ContentFile(buf.getvalue()), save=False)

        super(PFP, self).save(*args, **kwargs)

class ChatGroup(models.Model):
    name = models.CharField(max_length=32, unique=True)
    # current_online = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def last_message(self):
        if self.chat_messages.count() == 0:
            return None
        return self.chat_messages.first()


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.author.username, self.body)

    class Meta:
        ordering = ['-created']
