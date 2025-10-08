# FastAPI Backend

## 🧭 Overview

This repository is a **FastAPI-based REST backend** that uses **SQLAlchemy** for ORM, **Pydantic** (via `pydantic_settings`) for configuration, and **PostgreSQL** for data persistence.  
**Alembic** is included for database schema migrations.  

The application is structured in modular routers (for posts, users, authentication, and votes), providing clear separation of concerns and easy scalability.

---


## ⚙️ Tech Stack

| Component | Purpose |
|------------|----------|
| **Python 3.13.2** | Core programming language |
| **FastAPI** | Web framework for building APIs |
| **Uvicorn** | ASGI server for running the FastAPI app |
| **SQLAlchemy** | ORM layer for database interaction |
| **PostgreSQL** | Relational database |
| **Alembic** | Database migrations |
| **Pydantic Settings** | Environment variable management |
| **Docker + docker-compose** | Containerized setup for reproducible environments |

---


---

## ⚙️ Environment Configuration

The app reads configuration values using **Pydantic Settings** (from `app/config.py`), typically loaded from a `.env` file.

### Required environment variables

| Variable | Description |
|-----------|-------------|
| `DATABASE_HOSTNAME` | Hostname for the database (e.g., `postgres`) |
| `DATABASE_PORT` | Database port (default: `5432`) |
| `DATABASE_USERNAME` | Database username |
| `DATABASE_PASSWORD` | Database password |
| `DATABASE_NAME` | Database name |
| `SECRET_KEY` | Secret key for JWT token signing |
| `ALGORITHM` | Algorithm used for JWT (e.g., `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiry in minutes |

---

### Example `.env` (for local development)

> ⚠️ **Do NOT commit this file**. It should be listed in `.gitignore`.

```env
DATABASE_HOSTNAME=postgres
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=password123
DATABASE_NAME=fastapi

SECRET_KEY=replace_with_real_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🚀 Running the Project

**Create and activate a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Set environment variables (or use a .env file in the project root).**

**Run the FastAPI app**
```bash
uvicorn app.main:app --reload
```


**App will be available at** 👉 http://127.0.0.1:8000


