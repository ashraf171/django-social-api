from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User,Post,Like
# Create your tests here.

class PostTest(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(
            email="ashraf@test.com",
            username="ashraf",
            password="12345678",

        )
    def test_authenticated_user_can_create_post(self):
        self.client.force_authenticate(user=self.user)
        data={
            "title":"new post",
            "content":"hello from rest_framework"
        }

        response = self.client.post("/api/posts/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)
        self.assertEqual(Post.objects.first().title, "new post")
    
    def test_anonymous_user_cannot_create_post(self):
        data = {
        "title": "Unauthorized post",
        "content": "This should fail"
    }

        response = self.client.post("/api/posts/", data, format="json")

        self.assertIn(
        response.status_code,
        [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
    )
        self.assertEqual(Post.objects.count(), 0)


    def test_non_owner_cannot_update_post(self):
    
        user1 = User.objects.create_user(
        email="u1@test.com",
        username="u1",
        password="12345678",
    )
        user2 = User.objects.create_user(
        email="u2@test.com",
        username="u2",
        password="12345678",
    )

    
        post = Post.objects.create(
        author=user1,
        title="Original",
        content="Original content"
    )

    
        self.client.force_authenticate(user=user2)

    
        data = {
        "title": "Hacked",
        "content": "Hacked content"
        }

        response = self.client.patch(f"/api/posts/{post.id}/", data, format="json")

   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
        post.refresh_from_db()
        self.assertEqual(post.title, "Original")
    
    def test_user_can_like_and_unlike_post(self):
     user = User.objects.create_user(
        email="likeuser@test.com",
        username="likeuser",
        password="12345678",
    )

     post = Post.objects.create(
        author=user,
        title="Test post",
        content="Test content"
    )

     self.client.force_authenticate(user=user)

    
     response = self.client.post(f"/api/posts/{post.id}/like/")

     self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
     post.refresh_from_db()
     self.assertEqual(post.likes_count, 1)
     self.assertEqual(Like.objects.count(), 1)

    
     response = self.client.post(f"/api/posts/{post.id}/like/")

     self.assertEqual(response.status_code, status.HTTP_200_OK)
     post.refresh_from_db()
     self.assertEqual(post.likes_count, 0)
     self.assertEqual(Like.objects.count(), 0)


     def test_user_can_follow_and_unfollow_another_user(self):
        user1 = User.objects.create_user(
        email="user1@test.com",
        username="user1",
        password="12345678",
    )
        user2 = User.objects.create_user(
        email="user2@test.com",
        username="user2",
        password="12345678",
    )

        self.client.force_authenticate(user=user1)

   
        response = self.client.post(f"/api/follow/{user2.id}/")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

        user1.refresh_from_db()
        user2.refresh_from_db()
        self.assertEqual(user1.following_count, 1)
        self.assertEqual(user2.followers_count, 1)

       
        response = self.client.post(f"/api/unfollow/{user2.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user1.refresh_from_db()
        user2.refresh_from_db()
        self.assertEqual(user1.following_count, 0)
        self.assertEqual(user2.followers_count, 0)
