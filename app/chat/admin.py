from django.contrib import admin

from .models import User, PFP, ChatGroup, GroupMessage

admin.site.register(User)
admin.site.register(PFP)
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)

