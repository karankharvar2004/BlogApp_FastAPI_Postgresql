# 🚀 FastAPI Blog API (PostgreSQL)

A modern **Blog REST API** built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.
This project is a migration of a Django REST Framework (MongoDB) project to a high-performance FastAPI backend.

---

## 📌 Features

* ✅ Create, Read, Update, Delete (CRUD) Blog APIs
* ✅ Partial Update using `PATCH`
* ✅ PostgreSQL Database Integration
* ✅ SQLAlchemy ORM
* ✅ Pydantic Validation (like DRF serializers)
* ✅ Swagger UI (Interactive API Docs)
* ✅ Clean Project Structure (Production-ready)
* ✅ Environment Variables using `.env`
* ✅ Git-ready with proper `.gitignore`

---

## 🛠 Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Validation:** Pydantic
* **Server:** Uvicorn

---

## 📁 Project Structure

```
BLOGAPP/
│
├── blog/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── __init__.py
│       └── blog.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/karankharvar2004/BlogApp_Postgresql
cd your-repo
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup PostgreSQL

Create a database:

```sql
CREATE DATABASE blogdb;
```

---

### 5️⃣ Configure `.env`

Create `.env` file in root:

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/blogdb
```

---

### 6️⃣ Run Server

```bash
uvicorn blog.main:app --reload
```

---

## 🌐 API Documentation

After running server:

👉 Swagger UI:

```
http://127.0.0.1:8000/docs
```

## 📬 API Endpoints

### 🔹 Get All Blogs

```
GET /blogs/
```

---

### 🔹 Create Blog

```
POST /blogs/
```

**Request Body:**

```json
{
  "title": "Adventure Blog",
  "content": "Exciting travel story...",
  "author": "Karan"
}
```

---

### 🔹 Get Single Blog

```
GET /blogs/{blog_id}
```

---

### 🔹 Update Blog (Full)

```
PUT /blogs/{blog_id}
```

---

### 🔹 Update Blog (Partial)

```
PATCH /blogs/{blog_id}
```

**Example:**

```json
{
  "title": "Updated Title"
}
```

---

### 🔹 Delete Blog

```
DELETE /blogs/{blog_id}
```

---

## 🧠 Key Concepts

### 🔸 FastAPI vs DRF

| DRF          | FastAPI          |
| ------------ | ---------------- |
| Serializer   | Pydantic Schema  |
| APIView      | Router Functions |
| ORM (Django) | SQLAlchemy       |
| URL patterns | Decorators       |

---

### 🔸 PUT vs PATCH

| Method | Behavior               |
| ------ | ---------------------- |
| PUT    | Update entire object   |
| PATCH  | Update selected fields |

---

## 🧪 Testing

### ✅ Swagger UI

* Open `/docs`
* Click "Try it out"
* Execute APIs

### ✅ Postman

Use endpoints:

```
http://127.0.0.1:8000/blogs/
```

---

## ⚠️ Common Errors

| Error        | Reason                 |
| ------------ | ---------------------- |
| 422          | Invalid JSON           |
| 404          | Blog not found         |
| DB Error     | PostgreSQL not running |
| Import Error | Missing `__init__.py`  |

---

## 🔐 Environment Variables

Never commit `.env` file.
Use `.env.example` for sharing config.

---

## 👨‍💻 Author

**Karan**
Python Developer

---
