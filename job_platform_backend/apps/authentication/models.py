from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('job_poster', 'Job Poster'),
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='authentication_users_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email

user_permissions = models.ManyToManyField(
    'auth.Permission',
    related_name='authentication_on_user_permissions',
    blank=True,
    help_text='Specific permissions for this user.',
    verbose_name='user permissions',
)
