import json
import re
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from star_ratings.models import Rating, UserRating

from .models import Comment, Post


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # if self.scope["user"] == AnonymousUser():
        #     await self.close()
        #     return
        #
        # self.post_id = self.scope['url_route']['kwargs']['post_id']
        # self.room_group_name = f'comments_{self.post_id}'

        self.post_id = self.scope['url_route']['kwargs'].get('post_id')
        self.room_group_name = f"comments_{self.post_id}" if self.post_id else None

        if not self.scope["user"].is_authenticated:
            await self.close(code=4401)
            return

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

        # Send current rating to the newly connected client
        rating_data = await self.get_post_rating()
        await self.send(text_data=json.dumps({
            'type': 'current_rating',
            'rating': rating_data
        }))

    @database_sync_to_async
    def get_existing_comments(self):
        comments = Comment.objects.filter(post_id=self.post_id).order_by('-timestamp')
        return [{
            'id': comment.id,
            'user': {
                'id': comment.user.id,
                'name': comment.user.get_full_name() or comment.user.email,
                'avatar': comment.user.avatar.url if hasattr(comment.user, 'avatar') else None
            },
            'body': comment.body,
            'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'likes': comment.liked_by.count(),
            'mentions': [{
                'id': user.id,
                'name': user.get_full_name() or user.email
            } for user in comment.mentions.all()]
        } for comment in comments]

    @database_sync_to_async
    def get_post_rating(self):
        try:
            post = Post.objects.get(id=self.post_id)
            if post.ratings:
                rating = post.ratings
                # Get user's rating if user is authenticated
                user_rating = None
                if self.scope["user"].is_authenticated:
                    try:
                        user_rating_obj = UserRating.objects.get(
                            rating=rating,
                            user=self.scope["user"]
                        )
                        user_rating = user_rating_obj.score
                    except UserRating.DoesNotExist:
                        pass

                return {
                    'user_rating': user_rating,
                    'count': rating.count
                }
            return {
                'user_rating': None,
                'count': 0
            }
        except Post.DoesNotExist:
            return {
                'user_rating': None,
                'count': 0
            }

    async def disconnect(self, close_code):
        # Leave room group
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
        room = getattr(self, "room_group_name", None)
        if room:
            await self.channel_layer.group_discard(room, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        print(f"Received WebSocket message with action: {action}")

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
        elif action == 'delete_comment':
            delete_data = await self.delete_comment(text_data_json)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete_message',
                    'message': delete_data
                }
            )
        elif action == 'rate_post':
            print(f"Processing rating: {text_data_json}")
            rating_data = await self.save_rating(text_data_json)
            print(f"Rating data after save: {rating_data}")
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'rating_message',
                    'message': rating_data
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

    async def delete_message(self, event):
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

            # Process mentions in the comment body
            body = data['body']
            # Get mentioned users synchronously since we're in a sync_to_async context
            mentioned_users = self.process_mentions_sync(body)

            comment = Comment.objects.create(
                post=post,
                user=user,
                body=body
            )

            # Add mentions to the comment
            if mentioned_users:
                comment.mentions.set(mentioned_users)

            return {
                'id': comment.id,
                'user': {
                    'id': user.id,
                    'name': user.get_full_name() or user.email,
                    'avatar': user.avatar.url if hasattr(user, 'avatar') else None
                },
                'body': comment.body,
                'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'likes': 0,
                'mentions': [{
                    'id': user.id,
                    'name': user.get_full_name() or user.email
                } for user in mentioned_users]
            }

        except Exception as e:
            print(f"Error saving comment: {str(e)}")
            return {
                'error': str(e)
            }

    def process_mentions_sync(self, text):
        """Process @ mentions in the comment text and return list of mentioned users"""
        User = get_user_model()
        mentioned_users = []

        # Find all @mentions in the text
        mentions = re.findall(r'@([^@\s]+)', text)

        for mention in mentions:
            try:
                # Try to find user by full_name or email
                user = User.objects.filter(
                    models.Q(full_name__iexact=mention) |
                    models.Q(email__iexact=mention)
                ).first()
                if user:
                    mentioned_users.append(user)
            except User.DoesNotExist:
                continue

        return mentioned_users

    @database_sync_to_async
    def process_mentions(self, text):
        """Async wrapper for process_mentions_sync"""
        return self.process_mentions_sync(text)

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

    @database_sync_to_async
    def save_rating(self, data):
        try:
            user_id = data.get('user_id')
            rating_value = data.get('rating')

            if not user_id or not rating_value:
                raise ValueError("User ID and rating value are required")

            user = get_user_model().objects.get(id=user_id)
            post = Post.objects.get(id=self.post_id)

            # Get or create rating for the post
            content_type = ContentType.objects.get_for_model(post)

            rating, created = Rating.objects.get_or_create(
                content_type=content_type,
                object_id=post.id
            )

            # Update or create user rating
            user_rating, created = UserRating.objects.update_or_create(
                rating=rating,
                user=user,
                defaults={'score': rating_value}
            )

            # Update post's rating reference
            post.ratings = rating
            post.save()

            # Update rating count
            rating.count = UserRating.objects.filter(rating=rating).count()
            rating.save()

            result = {
                'user_rating': rating_value,
                'count': rating.count
            }
            print(f"Returning rating data: {result}")
            return result

        except Exception as e:
            print(f"Error saving rating: {str(e)}")
            return {
                'error': str(e)
            }

    @database_sync_to_async
    def delete_comment(self, data):
        """Delete a comment - users can only delete their own comments"""
        try:
            user_id = data.get('user_id')
            comment_id = data.get('comment_id')

            if not user_id or not comment_id:
                raise ValueError("User ID and Comment ID are required")

            user = get_user_model().objects.get(id=user_id)
            comment = Comment.objects.get(id=comment_id)

            # Check if the user owns this comment
            if comment.user != user:
                raise ValueError("You can only delete your own comments")

            # Store comment info before deletion
            comment_data = {
                'id': comment.id,
                'post_id': comment.post.id
            }

            # Delete the comment
            comment.delete()

            return {
                'success': True,
                'message': 'Comment deleted successfully',
                'comment_id': comment_id,
                'type': 'comment_deleted'
            }

        except Exception as e:
            print(f"Error deleting comment: {str(e)}")
            return {
                'error': str(e),
                'type': 'delete_error'
            }

    async def rating_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'rating_update',
            'rating': message
        }))
