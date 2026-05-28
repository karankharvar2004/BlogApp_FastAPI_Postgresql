# BlogApp FastAPI Backend

A production-style FastAPI backend project built with modular architecture, PostgreSQL, Docker, JWT Authentication, Alembic migrations, AWS S3 image uploads, and AWS CloudFront CDN integration.

---

# Features

- FastAPI backend architecture
- PostgreSQL database
- Async SQLAlchemy integration
- JWT Authentication
- Refresh token implementation
- Alembic database migrations
- Dockerized setup
- Docker Compose orchestration
- AWS S3 image upload support
- AWS CloudFront CDN integration
- Modular company-style architecture
- Soft delete implementation
- Swagger API documentation

---

# Tech Stack

## Backend
- FastAPI
- Python 3.13
- SQLAlchemy Async
- AsyncPG
- Alembic

## Authentication
- JWT Authentication

## Database
- PostgreSQL

## Cloud Services
- AWS S3
- AWS CloudFront

## DevOps
- Docker
- Docker Compose

---

# Project Structure

```bash
BlogApp Postgresql/
│
├── alembic/
├── src/
│   ├── database/
│   ├── services/
│   │   ├── users/
│   │   └── blogs/
│   ├── utils/
│   └── main.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md
```

---

# Features Implemented

## Authentication Module

- User Registration
- User Login
- JWT Access Token
- JWT Refresh Token
- Password Hashing

---

## Blog Module

- Create Blog
- Update Blog
- Delete Blog
- Fetch Single Blog
- Fetch All Blogs
- Blog Image Upload

---

## AWS S3 Integration

- Upload blog images to AWS S3
- Async image upload support
- Image deletion support

---

## AWS CloudFront Integration

Images are now served through CloudFront CDN instead of direct S3 URLs.

Benefits:
- Faster global image delivery
- Better caching
- Improved performance
- Production-style CDN architecture

---

# Docker Setup

## Clone Repository

```bash
git clone <your-github-repo-url>
```

---

## Move Into Project

```bash
cd "BlogApp Postgresql"
```

---

# Environment Variables

Create `.env` file in project root.

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/Blog_CompanyArc_DB

SECRET_KEY=your_secret_key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

REFRESH_TOKEN_EXPIRE_DAYS=7

AWS_ACCESS_KEY_ID=your_aws_access_key

AWS_SECRET_ACCESS_KEY=your_aws_secret_key

AWS_BUCKET_NAME=your_bucket_name

AWS_REGION=ap-south-1

CLOUDFRONT_URL=https://your-cloudfront-url.net
```

---

# Run Project Using Docker

## Build Containers

```bash
docker compose up --build
```

---

# Apply Alembic Migrations

Open new terminal:

```bash
docker exec -it blogapp_app alembic upgrade head
```

---

# Swagger Documentation

Open:

```text
http://localhost:8000/docs
```

---

# Docker Commands

## Start Containers

```bash
docker compose up
```

---

## Stop Containers

```bash
docker compose down
```

---

## Rebuild Containers

```bash
docker compose up --build
```

---

## View Running Containers

```bash
docker ps
```

---

## View Logs

```bash
docker logs -f blogapp_app
```

---

# Docker Hub Image

Pull Docker image:

```bash
docker pull karn21/blogapp-fastapi:latest
```

---

# CloudFront CDN

CloudFront distribution is integrated for image delivery.

Example image URL:

```text
https://your-cloudfront-domain/image.png
```

---

# API Documentation

Swagger UI available at:

```text
http://localhost:8000/docs
```

---

# Security Notes

- `.env` file is excluded from GitHub
- AWS credentials are managed using environment variables
- Docker containers are isolated
- JWT authentication implemented
- CloudFront used for secure CDN delivery

---

# Author

Karan Kharvar
