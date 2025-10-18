from django.core.management.base import BaseCommand
from apps.authentication.models import User
from apps.follows.models import Follow

class Command(BaseCommand):
    help = 'Test follow system functionality'
    
    def handle(self, *args, **options):
        self.stdout.write("🧪 TESTING FOLLOW SYSTEM...")
        
        # Create test users
        user1, created1 = User.objects.get_or_create(
            email='follow_test1@example.com',
            defaults={'user_type': 'job_seeker', 'password': 'test123'}
        )
        user2, created2 = User.objects.get_or_create(
            email='follow_test2@example.com', 
            defaults={'user_type': 'job_seeker', 'password': 'test123'}
        )
        
        if created1 or created2:
            self.stdout.write(f"✅ Created test users: {user1.id}, {user2.id}")
        
        # Test follow functionality
        follow, created = Follow.objects.get_or_create(
            follower=user1,
            following=user2
        )
        
        if created:
            self.stdout.write(f"✅ User {user1.id} now follows User {user2.id}")
        else:
            self.stdout.write(f"ℹ️  User {user1.id} already follows User {user2.id}")
        
        # Test getting followers
        user2_followers = Follow.objects.filter(following=user2)
        self.stdout.write(f"📊 User {user2.id} has {user2_followers.count()} followers")
        
        for follow in user2_followers:
            self.stdout.write(f"   - Follower: {follow.follower.email}")
        
        # Test getting following
        user1_following = Follow.objects.filter(follower=user1)
        self.stdout.write(f"📊 User {user1.id} is following {user1_following.count()} users")
        
        self.stdout.write("🎉 FOLLOW SYSTEM TEST COMPLETED!")