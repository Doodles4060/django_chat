import json
from channels.generic.websocket import WebsocketConsumer
from django.utils.timezone import datetime
from asgiref.sync import async_to_sync
import html
from django.core.cache import cache
from django.utils import formats
from django.utils.timezone import localtime

from .models import User, ChatGroup, GroupMessage


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        """
        Accepts user connection to the websocket server and adds them to the test chat group
        """
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        """
        Checks if online counter variable for the group exists in djangos cache and if not creates it with the default value of 0.
        Increments on a new user connection.
        
        P.S. Will be removed when Redis support is added.
        """
        if cache.get(f'group_{self.room_group_name}_count') is None:
            cache.set(f'group_{self.room_group_name}_count', 0)
        user_count = cache.incr('group_{}_count'.format(self.room_group_name), 1)

        """Sends notification when a new user joins the group"""
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'server_notification',
                'style': 'success',
                'message': 'New user just joined!',
                'user_count': user_count
            }
        )

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        """
        Receives and process new messages from users
        """
        text_data_json = json.loads(text_data)

        user = User.objects.get(pk=text_data_json['author'])
        group_pk = text_data_json['group']
        message = html.escape(text_data_json['message'])

        """
        If message is valid then save it to the database and send to the group chat. 
        Otherwise, handle the exception and make the user aware of it.
        """
        try:
            new_message = GroupMessage(
                author=user,
                group_id=group_pk,
                body=message
            )
            new_message.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'author': user.username,
                    'pfp': user.pfp.image.url,
                    'message': message,
                    'date_created': new_message.created
                }
            )
        except Exception as e:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'server_notification',
                    'style': 'danger',
                    'message': e.__str__()
                }
            )

    def disconnect(self, close_code):
        """
        Decreases user count and sends current value along with the notification that someone has left the chat
        """
        user_count = cache.get(f'group_{self.room_group_name}_count', 1)
        if user_count > 0:
            user_count = cache.decr(f'group_{self.room_group_name}_count', 1)
        else:
            cache.set(f'group_{self.room_group_name}_count', 0)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'server_notification',
                'style': 'danger',
                'message': 'Someone has just left',
                'user_count': user_count
            }
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def server_notification(self, event):
        message = event['message']
        style = event['style']

        if 'user_count' in event:
            user_count = event['user_count']
            self.send(text_data=json.dumps({
                'type': 'notification',
                'style': style,
                'message': message,
                'user_count': user_count
            }))
        else:
            self.send(text_data=json.dumps({
                'type': 'notification',
                'style': style,
                'message': message
            }))

    def chat_message(self, event):
        author = event['author']
        pfp = event['pfp']
        message = event['message']
        date_created = event['date_created'].isoformat()

        self.send(text_data=json.dumps({
            'type': 'chat',
            'author': author,
            'pfp': pfp,
            'message': message,
            'date_created': date_created
        }))
