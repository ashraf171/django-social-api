from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Like, Follow

User = get_user_model()

class PostTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="123456"
        )

    def test_authenticated_user_can_create_post(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Test post",
            "content": "Test content"
        }

        response = self.client.post("/api/posts/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    
    def test_unauthenticated_user_cannot_create_post(self):
        data = {
            "title": "Test post",
            "content": "Test content"
        }

        response = self.client.post("/api/posts/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_like_unlike_post(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.user,
            title="Post",
            content="Content"
        )

        # like
        response = self.client.post(f"/api/posts/{post.id}/like/")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.count(), 1)

        # unlike
        response = self.client.post(f"/api/posts/{post.id}/like/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.count(), 0)


class FollowTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@test.com",
            password="123456"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@test.com",
            password="123456"
        )

    def test_user_can_follow_and_unfollow(self):
        self.client.force_authenticate(user=self.user1)

    # follow
        response = self.client.post(f"/api/follow/{self.user2.id}/")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Follow.objects.count(), 1)

    # unfollow
        response = self.client.delete(f"/api/unfollow/{self.user2.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Follow.objects.count(), 0)

    def test_user_cannot_follow_himself(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(f"/api/follow/{self.user1.id}/")
        self.assertEqual(response.status_code, 400)

