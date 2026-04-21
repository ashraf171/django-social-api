from rest_framework import viewsets
from .serializers import PostSerializer,CommentSerializer,UserProfileSerializer,RegisterSerializer
from .models import Post,Comment,Like,Follow,User
from .permissions import IsCommentOwner,IsPostOwner
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from django.db.models import Prefetch
from django.db.models import Count


@extend_schema(description="Register a new user account")
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserProfileView(RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[AllowAny]



class MeView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serializer.data)

@extend_schema(description="Follow user")
class FollowUserView(APIView):
    def post(self, request, user_id):
        request_user = request.user
        target_user = get_object_or_404(User, id=user_id)

        if request_user == target_user:
            return Response(
                {'error': "you can't follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            obj, created = Follow.objects.get_or_create(
                follower=request_user,
                following=target_user
            )

            if created:
                target_user.followers_count += 1
                request_user.following_count += 1

                target_user.save()
                request_user.save()

                return Response({'message': "Followed"}, status=201)

        return Response({"message": "Already following"}, status=200)


@extend_schema(description="unfollow user")
class UnfollowUserView(APIView):
    def delete(self, request, user_id):
        request_user = request.user
        target_user = get_object_or_404(User, id=user_id)

        follow = Follow.objects.filter(
            follower=request_user,
            following=target_user
        ).first()

        if not follow:
            return Response({"error": "Not following"}, status=400)

        follow.delete()

        
        target_user.followers_count -= 1
        request_user.following_count -= 1

        target_user.save()
        request_user.save()

        return Response({"message": "Unfollowed"}, status=200)


class Pagination(PageNumberPagination):
    page_size=10

@extend_schema(description="List all posts or create a new post")
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').annotate(
    comments_count=Count('comments')
)
    permission_classes=[IsAuthenticatedOrReadOnly,IsPostOwner]
    serializer_class=PostSerializer
    pagination_class=Pagination
    filter_backends=[DjangoFilterBackend,SearchFilter]
    filterset_fields={ 'author': ['exact'],
    'title': ['exact', 'icontains'],
}
    search_fields=['title','content']
   
   

    
    
    @extend_schema(
    description="Like or unlike a post. If already liked, it will remove the like.",
    responses={200: {"type": "object", "example": {"status": "unlike"}},
               201: {"type": "object", "example": {"status": "liked"}}})
    
    @action(detail=True,methods=['post'],permission_classes=[IsAuthenticated])
    def like(self,request,pk=None):
        post=self.get_object()
        user=request.user
        like=Like.objects.filter(author=user,post=post).first()
        if like:
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            post.save()
            return Response({'status':'unlike'},status=status.HTTP_200_OK)
        else:
            Like.objects.create(author=user, post=post)
            post.likes_count += 1
            post.save()
            return Response(
                {"status": "liked"},
                status=status.HTTP_201_CREATED
            )
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request

        if request.user.is_authenticated:
            liked_post_ids = set(
            Like.objects.filter(author=request.user).values_list('post_id', flat=True)
            )
        context['liked_post_ids'] = liked_post_ids

        return context




class CommentViewSet(viewsets.ModelViewSet):
    pagination_class=Pagination
    queryset = Comment.objects.select_related('author', 'post', 'parent').order_by('-created_at')
    serializer_class=CommentSerializer



    def get_permissions(self):
        if self.action in ['update','partial_update','destroy']:
            return [IsCommentOwner()]
        return [IsAuthenticatedOrReadOnly()]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    



class FeedView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user

        return Post.objects.filter(
            author__followers__follower=user
        ).select_related('author').order_by('-created_at')