# views.py
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

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
            from django.apps import apps
            Job = apps.get_model('jobs', 'Job')  # Load Job model dynamically
            Application = apps.get_model('applications', 'Application')  # Load Application model dynamically
            
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