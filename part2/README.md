
# HBnB - BL and API (Part 2)

This repository contains the implementation of the Business Logic and API layers for the HBnB project, built using Python and Flask.

## ✅ Part 2 - Objectives

This part of the project focuses on implementing:
- A modular project structure
- Business logic classes for core entities
- A RESTful API using Flask and Flask-RESTX
- In-memory data persistence to simulate a database (for now)

---

## 📁 Project Structure

```
part2/
├── app/
│   ├── api/                  # Presentation Layer - Flask Routes
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── example.py
│   │
│   ├── core/                 # Business Logic Layer
│   │   ├── __init__.py
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       ├── user.py
│   │       ├── place.py
│   │       ├── review.py
│   │       └── amenity.py
│   │
│   ├── repository/           # Persistence Layer (In-Memory for now)
│   │   ├── __init__.py
│   │   └── in_memory_storage.py
│   │
│   └── core/facade.py        # Facade pattern connecting logic and API
│
├── run.py                    # Main entry point to start the Flask app
└── README.md                 # Project documentation
```

---

## 🚀 Task 0: Project Setup & Initialization

**What we did:**
- Created a clean modular architecture:
  - `api/` → Presentation layer
  - `core/` → Business logic layer
  - `repository/` → Persistence (in-memory)
- Implemented a working Flask app with test endpoint `/ping`
- Connected all layers using the **Facade Pattern**
- Built a reusable in-memory repository to simulate database operations

---

## 🧠 Task 1: Core Business Logic Classes

**We implemented the following models:**

### 🧱 BaseModel
The base class for all models.
- `id` (UUID)
- `created_at`, `updated_at` (timestamps)
- `to_dict()`: Converts object to JSON

### 👤 User
Represents an app user.
- `first_name`, `last_name`, `email`

### 📍 Place
Represents a place owned by a user.
- `name`, `description`, `address`
- `owner_id`
- `amenity_ids[]`, `review_ids[]`

### 📝 Review
Represents a review made by a user for a place.
- `text`
- `user_id`, `place_id`

### 🌿 Amenity
Represents a single feature/amenity.
- `name` (e.g., WiFi, Kitchen)

---

## 💡 Next Steps

- Implement full CRUD API endpoints for each entity
- Test endpoints using Postman or Swagger UI
- Prepare for future integration with a real database (SQLAlchemy)

---

## 🛠️ Tech Stack

- Python 3
- Flask
- Flask-RESTX
- UUIDs for entity identification

---

## 👥 Team & Attribution

This project is part of the Holberton program offered by **Tuwaiq Academy** in Saudi Arabia.

### Team Members:
- **Batoul Alsaeed**
- **Miad Alzhrani**
- **Rawan Albaraiki**

We worked collaboratively on the system design and implementation of the business logic and API architecture of the HBnB application.

---
