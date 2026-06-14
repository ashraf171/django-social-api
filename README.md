# Django Social Media API

[![Django Tests](https://github.com/ashraf171/django-social-api/actions/workflows/tests.yml/badge.svg)](https://github.com/ashraf171/django-social-api/actions/workflows/tests.yml)

A backend REST API for a social media platform built with Django REST Framework.

The project includes user registration, JWT authentication, posts, comments, replies, likes, follow/unfollow system, personalized feed, filtering, search, Swagger API documentation, Docker setup, and automated tests with GitHub Actions.

---

## Highlights

* Custom user model with email-based authentication
* JWT authentication using Simple JWT
* Posts CRUD with image support
* Comments and one-level replies
* Like / unlike system
* Follow / unfollow system
* Personalized feed based on followed users
* User profile and current user endpoints
* Filtering, search, and pagination
* Swagger and ReDoc API documentation
* Docker and Docker Compose setup
* Environment-based configuration
* Automated tests using GitHub Actions

---

## Tech Stack

* Python
* Django
* Django REST Framework
* Simple JWT
* PostgreSQL
* SQLite
* Docker
* Docker Compose
* GitHub Actions
* drf-spectacular / Swagger
* django-filter
* Pillow
* Gunicorn
* WhiteNoise

---

## Features

### Authentication

* User registration
* JWT login
* JWT refresh token
* Protected endpoints using authentication permissions

### Users

* Custom user model
* User profile endpoint
* Current authenticated user endpoint
* Followers and following counters
* Profile image and bio fields

### Posts

* Create, list, retrieve, update, and delete posts
* Only authenticated users can create posts
* Only post owners can update or delete their posts
* Post image support
* Likes count
* Comments count
* `is_liked` field for authenticated users

### Comments

* Create, list, retrieve, update, and delete comments
* Only comment owners can update or delete their comments
* One-level replies supported
* Validation prevents empty comments
* Validation prevents nested replies beyond one level

### Likes

* Authenticated users can like or unlike posts
* Duplicate likes are prevented
* Like count is updated safely

### Follow System

* Authenticated users can follow and unfollow other users
* Users cannot follow themselves
* Duplicate follows are prevented
* Followers and following counters are updated safely

### Feed

* Authenticated users can view a personalized feed
* Feed shows posts from users they follow
* Posts are ordered by newest first

---

## API Documentation

After running the project, API documentation is available at:

```text
http://localhost:8000/api/docs/
```

When running with Docker Compose, use:

```text
http://localhost:8001/api/docs/
```

Other documentation endpoints:

```text
/api/schema/
/api/redoc/
```

---

## Main API Endpoints

### Authentication

| Method | Endpoint              | Description                          |
| ------ | --------------------- | ------------------------------------ |
| POST   | `/api/register/`      | Register a new user                  |
| POST   | `/api/token/`         | Obtain JWT access and refresh tokens |
| POST   | `/api/token/refresh/` | Refresh JWT access token             |

### Users

| Method | Endpoint           | Description                    |
| ------ | ------------------ | ------------------------------ |
| GET    | `/api/me/`         | Get current authenticated user |
| GET    | `/api/users/{id}/` | Get user profile               |

### Posts

| Method    | Endpoint                | Description            |
| --------- | ----------------------- | ---------------------- |
| GET       | `/api/posts/`           | List posts             |
| POST      | `/api/posts/`           | Create post            |
| GET       | `/api/posts/{id}/`      | Retrieve post          |
| PUT/PATCH | `/api/posts/{id}/`      | Update post owner only |
| DELETE    | `/api/posts/{id}/`      | Delete post owner only |
| POST      | `/api/posts/{id}/like/` | Like or unlike a post  |

### Comments

| Method    | Endpoint              | Description               |
| --------- | --------------------- | ------------------------- |
| GET       | `/api/comments/`      | List comments             |
| POST      | `/api/comments/`      | Create comment            |
| GET       | `/api/comments/{id}/` | Retrieve comment          |
| PUT/PATCH | `/api/comments/{id}/` | Update comment owner only |
| DELETE    | `/api/comments/{id}/` | Delete comment owner only |

### Follow / Feed

| Method | Endpoint                   | Description           |
| ------ | -------------------------- | --------------------- |
| POST   | `/api/follow/{user_id}/`   | Follow user           |
| DELETE | `/api/unfollow/{user_id}/` | Unfollow user         |
| GET    | `/api/feed/`               | Get personalized feed |

---

## Filtering, Search, and Pagination

Posts support pagination, filtering, and search.

Examples:

```text
/api/posts/?page=2
/api/posts/?author=1
/api/posts/?title__icontains=django
/api/posts/?search=backend
```

---

## Authentication Header

For protected endpoints, send the JWT access token as a Bearer token:

```http
Authorization: Bearer your_access_token
```

---

## Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as a reference:

```env
SECRET_KEY=replace-with-your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Local development
DATABASE_URL=sqlite:///db.sqlite3

# Docker/PostgreSQL
POSTGRES_DB=social_db
POSTGRES_USER=social_user
POSTGRES_PASSWORD=social_password
DATABASE_URL=postgres://social_user:social_password@db:5432/social_db
```

Important:

```text
Do not commit the real .env file.
Only .env.example should be committed.
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ashraf171/django-social-api.git
cd django-social-api
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

For local SQLite development, make sure `.env` contains:

```env
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://localhost:8000/api/docs/
```

---

## Docker Setup

### 1. Create `.env`

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

For Docker, make sure `.env` contains:

```env
SECRET_KEY=dev-secret-key-for-local-docker
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

POSTGRES_DB=social_db
POSTGRES_USER=social_user
POSTGRES_PASSWORD=social_password

DATABASE_URL=postgres://social_user:social_password@db:5432/social_db
```

### 2. Build and run containers

```bash
docker compose up --build
```

The API will run at:

```text
http://localhost:8001/
```

Swagger documentation:

```text
http://localhost:8001/api/docs/
```

### 3. Stop containers

```bash
docker compose down
```

To remove containers and volumes:

```bash
docker compose down -v
```

---

## Running Tests

Run tests locally:

```bash
python manage.py test
```

The test suite covers:

* Authenticated post creation
* Unauthenticated post creation restriction
* Anonymous post listing
* Like / unlike behavior
* Like count updates
* Follow / unfollow behavior
* Preventing users from following themselves
* Preventing unauthenticated follow requests
* Preventing duplicate follow count increments

Tests are also executed automatically on every push and pull request using GitHub Actions.

---

## Project Structure

```text
django-social-api/
│
├── blog/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   └── tests.py
│
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .dockerignore
└── manage.py
```

---

## Project Status

This is a backend portfolio project focused on building and documenting a realistic REST API using Django REST Framework.

It demonstrates:

* API design
* Authentication
* Permissions
* Relational models
* Query optimization basics
* Testing
* Docker-based development
* CI with GitHub Actions
* API documentation

This project is intended as a portfolio-level backend API, not a full production social media platform.
