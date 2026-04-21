from rest_framework import serializers
from .models import Post,Comment,Like,User,Follow
from rest_framework.exceptions import ValidationError

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model=Comment
        fields=['id','author','author_username','post','content','parent','created_at','updated_at']
        read_only_fields=['id','author','created_at','updated_at']
    
    def validate(self, attrs):
        post = attrs.get('post')
        parent = attrs.get('parent')

        if parent and post and parent.post != post:
            raise serializers.ValidationError(
            "Parent comment must belong to the same post."
        )
        return attrs
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value
    
    def validate_parent(self, value):
        if value and value.parent is not None:
            raise ValidationError("Only one level of replies is allowed.")
        return value
       


class UserProfileSerializer(serializers.ModelSerializer):
    posts_count=serializers.SerializerMethodField()
    is_following=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['id',
                'username',
                'bio',
                'image',
                'followers_count',
                'following_count',
                'posts_count',
                'is_following']
        
    def get_posts_count(self,obj):
            return Post.objects.filter(author=obj).count()
        
    def get_is_following(self,obj):
            request=self.context.get('request')
            if not request or request.user.is_anonymous:
                return False
            
            return Follow.objects.filter(
                follower=request.user,
                following=obj).exists()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'image']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            image=validated_data.get('image', None),
        )
        return user
    



class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_username',
            'title',
            'content',
            'likes_count',
            'comments_count',
            'is_liked',
            'image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'author',
            'author_username',
            'likes_count',
            'comments_count',
            'is_liked',
            'created_at',
            'updated_at',
        ]


    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False

        liked_post_ids = self.context.get('liked_post_ids')
        if liked_post_ids is not None:
            return obj.id in liked_post_ids

        return Like.objects.filter(author=request.user, post=obj).exists()

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value




class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'author', 'post']
        read_only_fields = ['id', 'author']

    
    def validate(self, attrs):
        if Like.objects.filter(author=attrs['author'], post=attrs['post']).exists():
            raise ValidationError("You already liked this post.")
        return attrs
