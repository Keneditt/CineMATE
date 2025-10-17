# views.py
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer, SendMessageSerializer, UserBasicSerializer

User = get_user_model()

class MessageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        try:
            serializer = SendMessageSerializer(
                data=request.data, 
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            
            message = Message.objects.create(
                sender=request.user,
                receiver=serializer.validated_data['receiver'],
                content=serializer.validated_data['content']
            )
            
            response_serializer = MessageSerializer(message)
            return Response(
                {'message': response_serializer.data}, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {'error': f'Failed to send message: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='conversation/(?P<user_id>[^/.]+)')
    def get_conversation(self, request, user_id=None):
        try:
            other_user = get_object_or_404(User, id=user_id)
            
            # Generate conversation ID
            user_ids = sorted([request.user.id, other_user.id])
            conversation_id = f"{user_ids[0]}_{user_ids[1]}"
            
            messages = Message.objects.filter(
                conversation_id=conversation_id
            ).select_related(
                'sender__seeker_profile', 
                'receiver__seeker_profile'
            ).order_by('created_at')
            
            # Mark received messages as read
            Message.objects.filter(
                conversation_id=conversation_id,
                receiver=request.user,
                is_read=False
            ).update(is_read=True)
            
            serializer = MessageSerializer(messages, many=True)
            return Response({'messages': serializer.data})
            
        except Exception as e:
            return Response(
                {'error': f'Failed to get conversation: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def conversations(self, request):
        try:
            # Get unique conversations for current user
            conversations = Message.objects.filter(
                Q(sender=request.user) | Q(receiver=request.user)
            ).values('conversation_id').annotate(
                last_message_id=models.Max('id')
            ).order_by('-last_message_id')
            
            conversation_details = []
            
            for conv in conversations:
                last_message = Message.objects.get(id=conv['last_message_id'])
                user_ids = last_message.conversation_id.split('_')
                other_user_id = next(uid for uid in user_ids if int(uid) != request.user.id)
                other_user = get_object_or_404(User, id=other_user_id)
                
                unread_count = Message.objects.filter(
                    conversation_id=last_message.conversation_id,
                    receiver=request.user,
                    is_read=False
                ).count()
                
                conversation_details.append({
                    'conversation_id': last_message.conversation_id,
                    'last_message': MessageSerializer(last_message).data,
                    'other_user': UserBasicSerializer(other_user).data,
                    'unread_count': unread_count
                })
            
            return Response({'conversations': conversation_details})
            
        except Exception as e:
            return Response(
                {'error': f'Failed to get conversations: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['put'])
    def mark_read(self, request, pk=None):
        try:
            message = get_object_or_404(
                Message, 
                id=pk, 
                receiver=request.user
            )
            message.is_read = True
            message.save()
            
            return Response({'message': 'Message marked as read'})
            
        except Exception as e:
            return Response(
                {'error': f'Failed to mark message as read: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )