
# views.py
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .models import Follow, User
from .serializers import FollowSerializer, UserBasicSerializer

class FollowViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='follow/(?P<user_id>[^/.]+)')
    def follow_user(self, request, user_id=None):
        try:
            user_to_follow = get_object_or_404(User, id=user_id)
            
            if user_to_follow == request.user:
                return Response(
                    {'error': 'Cannot follow yourself'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            follow, created = Follow.objects.get_or_create(
                follower=request.user,
                following=user_to_follow
            )
            
            if not created:
                return Response(
                    {'error': 'Already following this user'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = FollowSerializer(follow)
            return Response(
                {'message': 'Successfully followed user', 'follow': serializer.data},
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {'error': f'Failed to follow user: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['delete'], url_path='unfollow/(?P<user_id>[^/.]+)')
    def unfollow_user(self, request, user_id=None):
        try:
            user_to_unfollow = get_object_or_404(User, id=user_id)
            follow = get_object_or_404(
                Follow, 
                follower=request.user, 
                following=user_to_unfollow
            )
            
            follow.delete()
            return Response({'message': 'Successfully unfollowed user'})
            
        except Exception as e:
            return Response(
                {'error': f'Failed to unfollow user: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='followers/(?P<user_id>[^/.]+)')
    def get_followers(self, request, user_id=None):
        try:
            user = get_object_or_404(User, id=user_id)
            followers = Follow.objects.filter(following=user).select_related(
                'follower__seeker_profile'
            )
            serializer = FollowSerializer(followers, many=True)
            return Response({'followers': serializer.data})
            
        except Exception as e:
            return Response(
                {'error': f'Failed to get followers: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='following/(?P<user_id>[^/.]+)')
    def get_following(self, request, user_id=None):
        try:
            user = get_object_or_404(User, id=user_id)
            following = Follow.objects.filter(follower=user).select_related(
                'following__seeker_profile'
            )
            serializer = FollowSerializer(following, many=True)
            return Response({'following': serializer.data})
            
        except Exception as e:
            return Response(
                {'error': f'Failed to get following: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#message_veiws.py
# views.py
from rest_framework.pagination import PageNumberPagination

class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 50

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = FeedPagination
    
    @action(detail=False, methods=['get'])
    def social(self, request):
        try:
            # Get users that current user is following
            following_ids = Follow.objects.filter(
                follower=request.user
            ).values_list('following_id', flat=True)
            
            if not following_ids:
                return Response({
                    'feed': [],
                    'pagination': {
                        'page': 1,
                        'limit': 10,
                        'total': 0,
                        'pages': 0
                    }
                })
            
            # Get jobs posted by followed users
            from job_creation.models import Job  # Import your Job model
            from django.apps import apps
            Application = apps.get_model('applications', 'Application')  # Get Application model dynamically
            
            followed_jobs = Job.objects.filter(
                poster_id__in=following_ids
            ).select_related('poster__seeker_profile').order_by('-created_at')
            
            # Get applications by followed users
            followed_applications = Application.objects.filter(
                seeker_id__in=following_ids
            ).select_related(
                'seeker__seeker_profile', 
                'job'
            ).order_by('-created_at')
            
            # Combine and paginate feed items
            feed_items = []
            
            for job in followed_jobs:
                feed_items.append({
                    'type': 'job_post',
                    'data': {
                        'id': job.id,
                        'title': job.title,
                        'description': job.description,
                        'poster': UserBasicSerializer(job.poster).data,
                        'created_at': job.created_at
                    },
                    'created_at': job.created_at
                })
            
            for app in followed_applications:
                feed_items.append({
                    'type': 'job_application',
                    'data': {
                        'id': app.id,
                        'proposal_message': app.proposal_message,
                        'seeker': UserBasicSerializer(app.seeker).data,
                        'job': {
                            'id': app.job.id,
                            'title': app.job.title
                        },
                        'created_at': app.created_at
                    },
                    'created_at': app.created_at
                })
            
            # Sort by creation date
            feed_items.sort(key=lambda x: x['created_at'], reverse=True)
            
            # Paginate
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(feed_items, request)
            
            return paginator.get_paginated_response({
                'feed': page,
                'pagination': {
                    'page': paginator.page.number,
                    'limit': paginator.page_size,
                    'total': len(feed_items),
                    'pages': paginator.page.paginator.num_pages
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to get social feed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
