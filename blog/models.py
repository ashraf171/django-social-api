from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='avatar_image/', blank=True, null=True)
    bio=models.TextField(blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    
    
    REQUIRED_FIELDS=['username']
    USERNAME_FIELD='email'
    def __str__(self):
        return self.username
    

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    title=models.CharField(max_length=225,db_index=True)
    content=models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to='posts_image/',blank=True,null=True)
    likes_count = models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}-{self.title}"


class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    content=models.TextField(blank=False)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name='replies')
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-created_at']

    def __str__(self):
       return f"{self.author.username} - {self.content[:20]}"
    

class Like(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['author', 'post'], name='unique_like')
        ]

    def __str__(self):
        return f"{self.author.username} Liked {self.post.author.username} Post "

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
       if self.follower == self.following:
            raise ValidationError("you can't follow your self")

    class Meta:
        unique_together = ('follower', 'following') 