# models.py
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_messages'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    conversation_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation_id']),
            models.Index(fields=['sender', 'receiver']),
        ]

    def save(self, *args, **kwargs):
        # Generate conversation ID (sorted to ensure consistency)
        user_ids = sorted([self.sender_id, self.receiver_id])
        self.conversation_id = f"{user_ids[0]}_{user_ids[1]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"