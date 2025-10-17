# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow, Message, ProfileSeeker

User = get_user_model()

class ProfileSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSeeker
        fields = ['full_name', 'tagline', 'bio', 'skills', 'location', 'profile_picture_url']

class UserBasicSerializer(serializers.ModelSerializer):
    seeker_profile = ProfileSeekerSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'seeker_profile']

class FollowSerializer(serializers.ModelSerializer):
    follower = UserBasicSerializer(read_only=True)
    following = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserBasicSerializer(read_only=True)
    receiver = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'is_read', 'conversation_id', 'created_at']

class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
    
    def validate(self, data):
        if data['receiver'] == self.context['request'].user:
            raise serializers.ValidationError("Cannot send message to yourself")
        return data

class FollowActionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()