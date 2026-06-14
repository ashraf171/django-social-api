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
        self.assertEqual(Post.objects.count(), 0)

    def test_like_unlike_post(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.user,
            title="Post",
            content="Content"
        )

        response = self.client.post(f"/api/posts/{post.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

        response = self.client.post(f"/api/posts/{post.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

    def test_anonymous_user_can_list_posts(self):
        Post.objects.create(
            author=self.user,
            title="Public post",
            content="Public content"
        )

        response = self.client.get("/api/posts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_unlike_updates_likes_count(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.user,
            title="Post",
            content="Content"
        )

        response = self.client.post(f"/api/posts/{post.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post.refresh_from_db()
        self.assertEqual(post.likes_count, 1)

        response = self.client.post(f"/api/posts/{post.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post.refresh_from_db()
        self.assertEqual(post.likes_count, 0)


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

        response = self.client.post(f"/api/follow/{self.user2.id}/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)

        self.user1.refresh_from_db()
        self.user2.refresh_from_db()

        self.assertEqual(self.user1.following_count, 1)
        self.assertEqual(self.user2.followers_count, 1)

        response = self.client.delete(f"/api/unfollow/{self.user2.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.count(), 0)

        self.user1.refresh_from_db()
        self.user2.refresh_from_db()

        self.assertEqual(self.user1.following_count, 0)
        self.assertEqual(self.user2.followers_count, 0)

    def test_user_cannot_follow_himself(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(f"/api/follow/{self.user1.id}/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Follow.objects.count(), 0)

    def test_unauthenticated_user_cannot_follow(self):
        response = self.client.post(f"/api/follow/{self.user2.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Follow.objects.count(), 0)

    def test_duplicate_follow_does_not_increment_counts(self):
        self.client.force_authenticate(user=self.user1)

        first_response = self.client.post(f"/api/follow/{self.user2.id}/")
        second_response = self.client.post(f"/api/follow/{self.user2.id}/")

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.count(), 1)

        self.user1.refresh_from_db()
        self.user2.refresh_from_db()

        self.assertEqual(self.user1.following_count, 1)
        self.assertEqual(self.user2.followers_count, 1)