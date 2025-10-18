#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_platform.settings')
django.setup()

from apps.authentication.models import User
from apps.follows.models import Follow
from apps.messages.models import Message
from apps.jobs.models import Job
from apps.applications.models import Application

def test_follow_system():
    print("🧪 TESTING FOLLOW SYSTEM")
    print("=" * 50)
    
    # Create users
    user1, created1 = User.objects.get_or_create(
        email='term_test1@example.com',
        defaults={'user_type': 'job_seeker', 'password': 'test123'}
    )
    user2, created2 = User.objects.get_or_create(
        email='term_test2@example.com',
        defaults={'user_type': 'job_seeker', 'password': 'test123'}
    )
    
    if created1:
        print(f"✅ Created user: {user1.email}")
    if created2:
        print(f"✅ Created user: {user2.email}")
    
    # Test follow
    follow, created = Follow.objects.get_or_create(follower=user1, following=user2)
    if created:
        print(f"✅ Follow created: {user1.id} -> {user2.id}")
    
    # Test data
    print(f"📊 {user2.email} has {user2.followers_set.count()} followers")
    print(f"📊 {user1.email} follows {user1.following_set.count()} users")
    
    print("🎉 FOLLOW SYSTEM TEST COMPLETED\n")

def test_messaging_system():
    print("🧪 TESTING MESSAGING SYSTEM") 
    print("=" * 50)
    
    user1 = User.objects.get(email='term_test1@example.com')
    user2 = User.objects.get(email='term_test2@example.com')
    
    # Send message
    message = Message.objects.create(
        sender=user1,
        receiver=user2, 
        content="Terminal test message - Hello!"
    )
    
    print(f"✅ Message sent: ID {message.id}")
    print(f"   From: {message.sender.email}")
    print(f"   To: {message.receiver.email}") 
    print(f"   Content: {message.content}")
    print(f"   Conversation ID: {message.conversation_id}")
    
    # Test conversation
    messages = Message.objects.filter(conversation_id=message.conversation_id)
    print(f"📨 Conversation has {messages.count()} messages")
    
    print("🎉 MESSAGING SYSTEM TEST COMPLETED\n")

def test_feed_simulation():
    print("🧪 TESTING FEED SIMULATION")
    print("=" * 50)
    
    user1 = User.objects.get(email='term_test1@example.com')
    user2 = User.objects.get(email='term_test2@example.com')
    
    # Create job from followed user
    job = Job.objects.create(
        poster=user2,
        title="Terminal Test Job",
        description="Created via terminal test",
        category="IT",
        budget_type="fixed", 
        budget_estimate=5000,
        location="Remote"
    )
    print(f"✅ Job created: {job.title}")
    
    # Create application
    app = Application.objects.create(
        job=job,
        seeker=user1,
        proposal_message="Applied via terminal test",
        status="pending"
    )
    print(f"✅ Application created")
    
    # Simulate feed generation
    following_ids = Follow.objects.filter(follower=user1).values_list('following_id', flat=True)
    followed_jobs = Job.objects.filter(poster_id__in=following_ids)
    followed_apps = Application.objects.filter(seeker_id__in=following_ids)
    
    print(f"🎯 FEED SIMULATION RESULTS:")
    print(f"   Users followed: {list(following_ids)}")
    print(f"   Jobs from followed users: {followed_jobs.count()}")
    print(f"   Applications from followed users: {followed_apps.count()}")
    
    for job in followed_jobs:
        print(f"     - Job: {job.title} by {job.poster.email}")
    
    print("🎉 FEED SIMULATION COMPLETED\n")

if __name__ == "__main__":
    print("🚀 STARTING TERMINAL-BASED BACKEND TESTS")
    print("=" * 60)
    
    test_follow_system()
    test_messaging_system() 
    test_feed_simulation()
    
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("💡 Check your database to see the test data created")