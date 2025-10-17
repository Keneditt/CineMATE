# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'follows', views.FollowViewSet, basename='follows')
router.register(r'messages', views.MessageViewSet, basename='messages')
router.register(r'feed', views.FeedViewSet, basename='feed')

urlpatterns = [
    path('api/', include(router.urls)),
]