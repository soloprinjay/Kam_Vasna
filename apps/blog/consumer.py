import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Comment, Post
from django.contrib.auth import get_user_model
from django.utils import timezone

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'comments_{self.post_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send existing comments to the newly connected client
        comments = await self.get_existing_comments()
        await self.send(text_data=json.dumps({
            'type': 'existing_comments',
            'comments': comments
        }))

    @database_sync_to_async
    def get_existing_comments(self):
        def get_replies(comment):
            replies = Comment.objects.filter(parent=comment).order_by('timestamp')
            return [{
                'id': reply.id,
                'user': {
                    'id': reply.user.id,
                    'name': reply.user.get_full_name() or reply.user.email,
                    'avatar': reply.user.avatar.url if hasattr(reply.user, 'avatar') else None
                },
                'body': reply.body,
                'timestamp': reply.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'parent_id': reply.parent.id,
                'likes': reply.liked_by.count(),
                'replies': get_replies(reply)  # Recursively get nested replies
            } for reply in replies]

        comments = Comment.objects.filter(post_id=self.post_id, parent=None).order_by('-timestamp')
        return [{
            'id': comment.id,
            'user': {
                'id': comment.user.id,
                'name': comment.user.get_full_name() or comment.user.email,
                'avatar': comment.user.avatar.url if hasattr(comment.user, 'avatar') else None
            },
            'body': comment.body,
            'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'parent_id': None,
            'likes': comment.liked_by.count(),
            'replies': get_replies(comment)
        } for comment in comments]

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action == 'new_comment':
            comment_data = await self.save_comment(text_data_json)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'comment_message',
                    'message': comment_data
                }
            )
        elif action == 'like_comment':
            like_data = await self.toggle_comment_like(text_data_json)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'like_message',
                    'message': like_data
                }
            )

    async def comment_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    async def like_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def save_comment(self, data):
        try:
            user_id = data.get('user_id')
            if not user_id:
                raise ValueError("User ID is required")

            # Convert user_id to integer
            try:
                user_id = int(user_id)
            except (ValueError, TypeError):
                raise ValueError("Invalid user ID format")

            user = get_user_model().objects.get(id=user_id)
            post = Post.objects.get(id=self.post_id)

            parent = None
            if data.get('parent_id'):
                try:
                    parent_id = int(data['parent_id'])
                    parent = Comment.objects.get(id=parent_id)
                except (ValueError, TypeError):
                    raise ValueError("Invalid parent comment ID format")
                except Comment.DoesNotExist:
                    parent = None

            comment = Comment.objects.create(
                post=post,
                user=user,
                body=data['body'],
                parent=parent
            )

            return {
                'id': comment.id,
                'user': {
                    'id': user.id,
                    'name': user.get_full_name() or user.email,
                    'avatar': user.avatar.url if hasattr(user, 'avatar') else None
                },
                'body': comment.body,
                'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'parent_id': parent.id if parent is not None else None,
                'likes': 0
            }

        except Exception as e:
            print(f"Error saving comment: {str(e)}")
            return {
                'error': str(e)
            }

    @database_sync_to_async
    def toggle_comment_like(self, data):
        try:
            user_id = data.get('user_id')
            comment_id = data.get('comment_id')
            
            if not user_id or not comment_id:
                raise ValueError("User ID and Comment ID are required")

            user = get_user_model().objects.get(id=user_id)
            comment = Comment.objects.get(id=comment_id)
            
            # Toggle like
            if user in comment.liked_by.all():
                comment.liked_by.remove(user)
                liked = False
            else:
                comment.liked_by.add(user)
                liked = True

            return {
                'comment_id': comment.id,
                'likes': comment.liked_by.count(),
                'liked': liked
            }

        except Exception as e:
            print(f"Error toggling comment like: {str(e)}")
            return {
                'error': str(e)
            }
