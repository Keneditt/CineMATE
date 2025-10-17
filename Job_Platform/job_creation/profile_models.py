# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSeeker(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='seeker_profile'
    )
    full_name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.full_name}"