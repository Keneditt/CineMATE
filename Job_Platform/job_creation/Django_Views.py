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