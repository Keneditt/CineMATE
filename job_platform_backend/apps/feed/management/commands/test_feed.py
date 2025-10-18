from django.core.management.base import BaseCommand
from apps.authentication.models import User
from apps.follows.models import Follow
from apps.jobs.models import Job
from apps.applications.models import Application

class Command(BaseCommand):
    help = 'Test social feed functionality'
    
    def handle(self, *args, **options):
        self.stdout.write("🧪 TESTING SOCIAL FEED...")
        
        # Get or create test users
        user1, _ = User.objects.get_or_create(
            email='feed_test1@example.com',
            defaults={'user_type': 'job_seeker', 'password': 'test123'}
        )
        user2, _ = User.objects.get_or_create(
            email='feed_test2@example.com',
            defaults={'user_type': 'job_poster', 'password': 'test123'}
        )
        
        # Make user1 follow user2
        Follow.objects.get_or_create(follower=user1, following=user2)
        self.stdout.write(f"✅ {user1.email} now follows {user2.email}")
        
        # Create a job from user2
        job, created = Job.objects.get_or_create(
            poster=user2,
            title="Senior Python Developer",
            description="Looking for experienced Python developer",
            category="IT",
            budget_type="fixed",
            budget_estimate=5000,
            location="Remote"
        )
        
        if created:
            self.stdout.write(f"✅ Created job: {job.title}")
        
        # Create an application from user1
        application, app_created = Application.objects.get_or_create(
            job=job,
            seeker=user1,
            defaults={
                'proposal_message': 'I am interested in this position!',
                'status': 'pending'
            }
        )
        
        if app_created:
            self.stdout.write(f"✅ Created application for job")
        
        # Simulate feed generation
        following_ids = Follow.objects.filter(follower=user1).values_list('following_id', flat=True)
        
        self.stdout.write(f"📊 Users that {user1.email} follows: {list(following_ids)}")
        
        # Get jobs from followed users
        followed_jobs = Job.objects.filter(poster_id__in=following_ids)
        self.stdout.write(f"📋 Jobs from followed users: {followed_jobs.count()}")
        
        for job in followed_jobs:
            self.stdout.write(f"   - {job.title} by {job.poster.email}")
        
        # Get applications from followed users
        followed_apps = Application.objects.filter(seeker_id__in=following_ids)
        self.stdout.write(f"📝 Applications from followed users: {followed_apps.count()}")
        
        self.stdout.write("🎉 SOCIAL FEED TEST COMPLETED!")