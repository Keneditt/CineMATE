from django.core.management.base import BaseCommand
from apps.authentication.models import User
from apps.chat.models import Message

class Command(BaseCommand):
    help = 'Test messaging system functionality'
    
    def handle(self, *args, **options):
        self.stdout.write("🧪 TESTING MESSAGING SYSTEM...")
        
        # Get or create test users
        user1, _ = User.objects.get_or_create(
            email='msg_test1@example.com',
            defaults={'user_type': 'job_seeker', 'password': 'test123'}
        )
        user2, _ = User.objects.get_or_create(
            email='msg_test2@example.com',
            defaults={'user_type': 'job_seeker', 'password': 'test123'}
        )
        
        # Test sending message
        message = Message.objects.create(
            sender=user1,
            receiver=user2,
            content="Hello! This is a test message from the terminal."
        )
        
        self.stdout.write(f"✅ Message sent: ID {message.id}")
        self.stdout.write(f"   From: {message.sender.email}")
        self.stdout.write(f"   To: {message.receiver.email}") 
        self.stdout.write(f"   Content: {message.content}")
        self.stdout.write(f"   Conversation ID: {message.conversation_id}")
        
        # Test conversation retrieval
        conversation_messages = Message.objects.filter(
            conversation_id=message.conversation_id
        ).order_by('created_at')
        
        self.stdout.write(f"📊 Conversation has {conversation_messages.count()} messages")
        
        # Test unread messages
        unread_count = Message.objects.filter(
            receiver=user2,
            is_read=False
        ).count()
        self.stdout.write(f"📨 User {user2.email} has {unread_count} unread messages")
        
        self.stdout.write("🎉 MESSAGING SYSTEM TEST COMPLETED!")