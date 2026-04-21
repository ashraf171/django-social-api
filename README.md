# Social Media API

A RESTful social media API built with Django and Django REST Framework.
It allows users to create posts, comment, like, follow other users, and view a personalized feed.

---

## Features

* User authentication using JWT
* Create, update, and delete posts
* Comment on posts and reply to comments
* Like and unlike posts
* Follow and unfollow users
* Personalized feed based on following
* User profile with followers and posts count
* Permissions system (owner-based access control)

---

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite

---

## Installation

```bash
git clone https://github.com/ashraf171/django-social-api
cd django-social-api
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Authentication

### Get Token

```http
POST /api/token/
```

### Refresh Token

```http
POST /api/token/refresh/
```

### Use Token in Requests

```http
Authorization: Bearer your_access_token
```

---

## Example Request

### Create a Post

```http
POST /api/posts/
Authorization: Bearer your_access_token
Content-Type: application/json
```

```json
{
  "title": "My first post",
  "content": "Hello from Django REST Framework"
}
```

---

## Example Response

```json
{
  "id": 1,
  "author": 1,
  "author_username": "ashraf",
  "title": "My first post",
  "content": "Hello from Django REST Framework",
  "likes_count": 0,
  "comments_count": 0,
  "comments": [],
  "is_liked": false,
  "image": null,
  "created_at": "2026-04-20T10:00:00Z",
  "updated_at": "2026-04-20T10:00:00Z"
}
```

---

## Image Upload

To upload an image with a post, use `form-data`:

* title → Text
* content → Text
* image → File

---

## API Endpoints

### Posts

* GET /api/posts/
* POST /api/posts/
* GET /api/posts/{id}/
* PUT /api/posts/{id}/
* DELETE /api/posts/{id}/
* POST /api/posts/{id}/like/

---

### Comments

* GET /api/comments/
* POST /api/comments/
* GET /api/comments/{id}/
* PUT /api/comments/{id}/
* DELETE /api/comments/{id}/

---

### Users

* GET /api/users/{id}/
* GET /api/me/

---

### Follow System

* POST /api/users/{id}/follow/

---

### Feed

* GET /api/feed/
