from rest_framework.routers import DefaultRouter
from .views import PostViewSet,CommentViewSet,FollowUserView,UnfollowUserView,FeedView,UserProfileView, MeView,RegisterView
from django.urls import path,include
router=DefaultRouter()

router.register(r'posts',PostViewSet,basename='posts')
router.register(r'comments',CommentViewSet,basename='comments')

urlpatterns=[
    path('',include(router.urls)),
    path('feed/',FeedView.as_view(),name='feed'),
    path('follow/<int:user_id>/',FollowUserView.as_view(),name='follow-user'),
    path('unfollow/<int:user_id>/',UnfollowUserView.as_view(),name='unfollow-user'),
    path('users/<int:pk>/',UserProfileView.as_view(),name='user-profile'),
    path('me/',MeView.as_view(),name='me'),
    path('register/', RegisterView.as_view(), name='register'),
]


