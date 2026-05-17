# FitTrack - Full Stack Workout Tracker

## 📌 Project Description

FitTrack is a full-stack web application that allows users to register, log in, and manage their personal workouts. Each user can create, view, update, and delete their own workout records.

The project was built as a capstone assignment using Flask for the backend and React for the frontend, focusing on authentication, user-specific data, and full CRUD functionality.

---

## 🚀 Features

- User registration and login system
- JWT-based authentication
- Protected routes (only logged-in users can access dashboard)
- Create, read, update, and delete workouts (CRUD)
- Each user can only access their own workouts
- Simple and responsive frontend UI
- Secure password hashing using bcrypt

---

## 🛠 Tech Stack

### Backend:

- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt
- Flask-CORS
- SQLite

### Frontend:

- React
- JavaScript (ES6+)
- React Router
- Fetch API

---

## 🔐 Authentication Flow

- User registers with username and password
- Password is hashed before saving to the database
- On login, a JWT token is generated
- Token is stored in localStorage on the frontend
- All protected routes require the token to access data

---

## 📡 API Routes

### Auth Routes

- `POST /api/register` → Create a new user
- `POST /api/login` → Login user and return JWT token

### Workout Routes (Protected)

- `GET /api/workouts` → Get all workouts for logged-in user
- `POST /api/workouts` → Create a new workout
- `PATCH /api/workouts/<id>` → Update workout
- `DELETE /api/workouts/<id>` → Delete workout

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd fittrack-project
```
