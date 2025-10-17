# models.py - Add methods to User model or create UserManager
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserManager(models.Manager):
    def get_followers(self, user_id):
        return User.objects.filter(
            followers_set__follower_id=user_id
        ).select_related('seeker_profile')
    
    def get_following(self, user_id):
        return User.objects.filter(
            following_set__following_id=user_id
        ).select_related('seeker_profile')