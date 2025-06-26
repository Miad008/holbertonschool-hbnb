
# HBnB - BL and API (Part 2)

This repository contains the implementation of the **Business Logic (BL)** and **RESTful API** layers for the HBnB project, developed as part of the Holberton curriculum at **Tuwaiq Academy**.

## ✅ Part 2 - Objectives

* Create a modular, maintainable project structure.
* Implement business logic for core entities.
* Develop RESTful APIs using Flask and Flask-RESTx.
* Simulate data persistence using an in-memory repository.
* Validate data, test endpoints, and ensure API reliability.

---

## 📁 Project Structure

```
holbertonschool-hbnb/
├── part2/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── amenities.py
│   │   │       ├── places.py
│   │   │       ├── reviews.py
│   │   │       └── users.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── amenity.py
│   │   │   ├── place.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── facade.py
│   │   └── persistence/
│   │       ├── __init__.py
│   │       ├── in_memory_storage.py
│   │       └── storage_interface.py
│   ├── run.py
│   └── README.md
├── tests/
│   ├── __init__.py
│   ├── test_api_amenities.py
│   ├── test_api_places.py
│   ├── test_api_reviews.py
│   └── test_api_users.py
├── requirements.txt
└── .gitignore
```
---

## ⚙️ Setup & Configuration

The configuration is handled via `config.py`, which supports environment-based setup using classes:

```python
# part2/app/config.py

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
```

You can apply the config in __init__.py using:
```bash
app.config.from_object(Config)
```
To run the app locally:
```bash
python3 part2/run.py
```

------

## 🚀 API Endpoints

Implemented using **Flask-RESTx**, fully documented via **Swagger UI**:

| Method | Endpoint                          | Description                        |
|--------|-----------------------------------|------------------------------------|
| POST   | `/api/v1/users/`                  | Create a new user                  |
| GET    | `/api/v1/users/`                  | Retrieve all users                 |
| POST   | `/api/v1/places/`                 | Create a new place                 |
| GET    | `/api/v1/places/`                 | Retrieve all places                |
| POST   | `/api/v1/reviews/`                | Create a new review                |
| GET    | `/api/v1/reviews/`                | Retrieve all reviews               |
| POST   | `/api/v1/amenities/`              | Create a new amenity               |
| GET    | `/api/v1/amenities/`              | Retrieve all amenities             |
| GET    | `/api/v1/places/<place_id>/reviews/` | Retrieve reviews for a place   |
| PUT    | `/api/v1/reviews/<review_id>`     | Update a review by ID              |
| DELETE | `/api/v1/reviews/<review_id>`     | Delete a review by ID              |


📄 Swagger Docs: `http://127.0.0.1:5000/api/v1/`

------

## ✅ Validation Logic

All models perform internal data validation to ensure data integrity:
**User**: Requires first_name, last_name, and valid email.
**Place**: Requires title, positive price, and valid latitude/longitude
**Review**: Requires text, valid user_id, and place_id
**Amenity**: Requires non-empty name (max 50 characters)

---

## 🧪 Testing


* Manual testing via `curl` and Swagger
* Automated testing using `unittest`
* Test coverage includes:

  * Valid and invalid inputs
  * Missing fields
  * Boundary value checks

### 🧪 Example Command

```bash
python3 -m unittest discover -s tests
```

### ✅ Sample Output

```bash
----------------------------------------------------------------------
Ran 13 tests in 0.093s

OK
```

---

## ⚠️ Issues Faced & Fixes

| Issue                            | Fix                                                      |
| -------------------------------- | -------------------------------------------------------- |
| `ModuleNotFoundError` for config | Corrected import path: `from part2.config import Config` |
| Missing `name` in POST requests  | Added field validation in business logic                 |
| In-memory storage errors         | Handled default values and object references properly    |

---

## 📌 Notes
* This project uses an in-memory repository (no database).
* All APIs are accessible and testable via Swagger.
* The app is structured following clean architecture and separation of concerns.

---

## 🛠️ Tech Stack

* Python 3
* Flask
* Flask-RESTx
* UUID
* Unittest

---

## 💡 Future Improvements

* Switch from in-memory to persistent database (e.g. PostgreSQL)
* Add authentication and authorization
* CI/CD integration for automated tests

---

## 👥 Team & Attribution

Developed as part of the *Holberton* program at **Tuwaiq Academy**:

* **Batoul Alsaeed**
* **Miad Alzhrani**
* **Rawan Albaraiki**

We worked collaboratively on the system design, development, testing, and documentation.

--
