from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Post, Like, Follow, Comment


User = get_user_model()


class ApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ashraf",
            email="ashraf@ashraf.com",
            password="1234",
        )

        self.other_user = User.objects.create_user(
            username="other",
            email="other@test.com",
            password="1234",
        )

    def test_non_owner_cannot_update_post(self):
        self.client.force_authenticate(user=self.other_user)

        post = Post.objects.create(
            author=self.user,
            title="django",
            content="django is a amazing frame work",
        )

        data = {"title": "New Title"}

        response = self.client.patch(
            f"/api/posts/{post.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        post.refresh_from_db()
        self.assertEqual(post.title, "django")

    def test_owner_can_delete_own_post(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.user,
            title="django",
            content="django is a amazing frame work !",
        )

        response = self.client.delete(f"/api/posts/{post.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_non_owner_cannot_delete_post(self):
        self.client.force_authenticate(user=self.other_user)

        post = Post.objects.create(
            author=self.user,
            title="django is good",
            content="good night",
        )

        response = self.client.delete(f"/api/posts/{post.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)

    def test_unauthenticated_user_cannot_update_post(self):
        post = Post.objects.create(
            author=self.user,
            title="django",
            content="likely",
        )

        data = {"title": "New Title"}

        response = self.client.patch(
            f"/api/posts/{post.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        post.refresh_from_db()
        self.assertEqual(post.title, "django")

    def test_authenticated_user_can_create_comment(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.other_user,
            title="dd",
            content="ff",
        )

        data = {
            "post": post.id,
            "content": "Nice post",
        }

        response = self.client.post(
            "/api/comments/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.first()
        self.assertEqual(comment.content, "Nice post")
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.author, self.user)

    def test_unauthenticated_user_cannot_create_comment(self):
        post = Post.objects.create(
            author=self.user,
            title="dd",
            content="ff",
        )

        data = {
            "post": post.id,
            "content": "Nice post",
        }

        response = self.client.post(
            "/api/comments/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), 0)

    def test_owner_can_delete_own_comment(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.other_user,
            title="DD",
            content="FFF",
        )

        comment = Comment.objects.create(
            author=self.user,
            content="Nice Post",
            post=post,
        )

        response = self.client.delete(f"/api/comments/{comment.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_non_owner_cannot_delete_comment(self):
        self.client.force_authenticate(user=self.other_user)

        post = Post.objects.create(
            author=self.user,
            title="FFF",
            content="ddd",
        )

        comment = Comment.objects.create(
            author=self.user,
            content="Nice",
            post=post,
        )

        response = self.client.delete(f"/api/comments/{comment.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)

    def test_owner_can_update_own_comment(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.other_user,
            title="django",
            content="amazing",
        )

        comment = Comment.objects.create(
            author=self.user,
            post=post,
            content="nice",
        )

        data = {"content": "Updated comment"}

        response = self.client.patch(
            f"/api/comments/{comment.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        comment.refresh_from_db()
        self.assertEqual(comment.content, "Updated comment")

    def test_non_owner_cannot_update_comment(self):
        self.client.force_authenticate(user=self.other_user)

        post = Post.objects.create(
            author=self.user,
            title="gg",
            content="GG",
        )

        comment = Comment.objects.create(
            author=self.user,
            post=post,
            content="Nice",
        )

        data = {"content": "Update content"}

        response = self.client.patch(
            f"/api/comments/{comment.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        comment.refresh_from_db()
        self.assertEqual(comment.content, "Nice")

    def test_unauthenticated_user_cannot_update_comment(self):
        post = Post.objects.create(
            author=self.user,
            title="GG",
            content="GGG",
        )

        comment = Comment.objects.create(
            author=self.user,
            post=post,
            content="Nice",
        )

        data = {"content": "Updated by anonymous"}

        response = self.client.patch(
            f"/api/comments/{comment.id}/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        comment.refresh_from_db()
        self.assertEqual(comment.content, "Nice")

    def test_authenticated_user_cannot_create_comment_without_content(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.user,
            title="ff",
            content="LL",
        )

        data = {"post": post.id}

        response = self.client.post(
            "/api/comments/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

    def test_authenticated_user_cannot_create_comment_with_invalid_post(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "post": 99999,
            "content": "Hello",
        }

        response = self.client.post(
            "/api/comments/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

    def test_authenticated_user_cannot_create_comment_with_blank_content(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.user,
            title="GGG",
            content="TTRR",
        )

        data = {
            "post": post.id,
            "content": "",
        }

        response = self.client.post(
            "/api/comments/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

    def test_authenticated_user_can_like_post(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.user,
            title="GGG",
            content="DDD",
        )

        response = self.client.post(f"/api/posts/{post.id}/like/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

        like = Like.objects.first()
        self.assertEqual(like.author, self.user)
        self.assertEqual(like.post, post)

    def test_second_like_unlikes_post(self):
        self.client.force_authenticate(user=self.user)

        post = Post.objects.create(
            author=self.user,
            title="GGG",
            content="DDD",
            likes_count=1,
        )

        Like.objects.create(
            author=self.user,
            post=post,
        )

        response = self.client.post(f"/api/posts/{post.id}/like/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

        post.refresh_from_db()
        self.assertEqual(post.likes_count, 0)

    def test_unauthenticated_user_cannot_like_post(self):
        post = Post.objects.create(
            author=self.user,
            title="GG",
            content="FFF",
        )

        response = self.client.post(f"/api/posts/{post.id}/like/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Like.objects.count(), 0)

        post.refresh_from_db()
        self.assertEqual(post.likes_count, 0)

    def test_authenticated_user_can_follow_another_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f"/api/follow/{self.other_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)

        follow = Follow.objects.first()
        self.assertEqual(follow.follower, self.user)
        self.assertEqual(follow.following, self.other_user)

    def test_unauthenticated_user_cannot_follow_another_user(self):
        response = self.client.post(f"/api/follow/{self.other_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Follow.objects.count(), 0)

    def test_user_cannot_follow_himself(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f"/api/follow/{self.user.id}/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Follow.objects.count(), 0)

    def test_authenticated_user_can_unfollow_another_user(self):
        self.client.force_authenticate(user=self.user)

        Follow.objects.create(
            follower=self.user,
            following=self.other_user,
        )

        self.assertEqual(Follow.objects.count(), 1)

        response = self.client.delete(f"/api/unfollow/{self.other_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.count(), 0)

    def test_unauthenticated_user_cannot_unfollow_another_user(self):
        Follow.objects.create(
            follower=self.user,
            following=self.other_user,
        )

        self.assertEqual(Follow.objects.count(), 1)

        response = self.client.delete(f"/api/unfollow/{self.other_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Follow.objects.count(), 1)

    def test_user_cannot_follow_same_user_twice(self):
        self.client.force_authenticate(user=self.user)

        Follow.objects.create(
            follower=self.user,
            following=self.other_user,
        )

        self.assertEqual(Follow.objects.count(), 1)

        response = self.client.post(f"/api/follow/{self.other_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Already following")
        self.assertEqual(Follow.objects.count(), 1)

    def test_unfollow_when_not_following_returns_400(self):
        self.client.force_authenticate(user=self.user)

        self.assertEqual(Follow.objects.count(), 0)

        response = self.client.delete(f"/api/unfollow/{self.other_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Follow.objects.count(), 0)

    def test_follow_increases_followers_and_following_count(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f"/api/follow/{self.other_user.id}/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 1)

        self.user.refresh_from_db()
        self.other_user.refresh_from_db()

        self.assertEqual(self.user.following_count, 1)
        self.assertEqual(self.other_user.followers_count, 1)
