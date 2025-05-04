import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Comment, Post
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_slug = self.scope['url_route']['kwargs']['post_slug']
        self.room_group_name = f'comments_{self.post_slug}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment_text = text_data_json['comment']
        rating = text_data_json.get('rating', 0)
        user_id = text_data_json.get('user_id')

        # Save comment to database
        comment = await self.save_comment(comment_text, rating, user_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_message',
                'comment': {
                    'id': comment.id,
                    'text': comment.body,
                    'rating': comment.rating,
                    'user_name': comment.name,
                    'created': comment.created.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }
        )

    async def comment_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['comment']))

    @database_sync_to_async
    def save_comment(self, comment_text, rating, user_id):
        post = Post.objects.get(slug=self.post_slug)
        user = User.objects.get(id=user_id) if user_id else None
        
        comment = Comment.objects.create(
            post=post,
            name=user.username if user else 'Anonymous',
            email=user.email if user else 'anonymous@example.com',
            body=comment_text,
            rating=rating
        )
        return comment 