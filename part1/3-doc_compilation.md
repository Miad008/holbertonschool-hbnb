## HBnB Evolution - Technical Documentation

### 📌 Introduction

This document outlines the core architectural and design components of the HBnB Evolution project, a simplified version of an AirBnB-like application. It compiles all technical diagrams and notes to guide the implementation phase and ensure clear understanding of the system.

---

### 🧱 High-Level Architecture

#### 📦 Package Diagram:

```mermaid
flowchart TD
 subgraph subGraph0["Presentation Layer"]
        A["ServiceAPI"]
  end
 subgraph subGraph1["Business Logic Layer"]
        B["Facade"]
        C["User"]
        D["Place"]
        E["Review"]
        F["Amenity"]
  end
 subgraph subGraph2["Persistence Layer"]
        G["DBStorage"]
  end
    A --> B
    B --> C & D & E & F & G
```

#### 📝 Explanation:

* **Presentation Layer**: Interfaces where users interact with the system through APIs or UIs.
* **Business Logic Layer**: Contains the core app logic, including entities and rules.
* **Persistence Layer**: Handles communication with the database.
* **Facade Pattern**: Simplifies interaction between presentation and logic layers.

---

### 📚 Business Logic Layer - Class Diagram

```mermaid
classDiagram
    class User {
        +UUID id
        +String email
        +String password
        +String first_name
        +String last_name
        +String role
        +datetime created_at
        +datetime updated_at
    }

    class Place {
        +UUID id
        +String title
        +String description
        +float price
        +float latitude
        +float longitude
        +datetime created_at
        +datetime updated_at
    }

    class Review {
        +UUID id
        +int rating
        +String comment
        +datetime created_at
        +datetime updated_at
    }

    class Amenity {
        +UUID id
        +String name
        +String description
        +datetime created_at
        +datetime updated_at
    }

    User "1" -- "0..*" Place : owns
    User "1" -- "0..*" Review : writes
    Place "1" -- "0..*" Review : receives
    Place "1" -- "0..*" Amenity : has
```

#### 📝 Explanation:

Each class includes essential attributes like ID, creation/update time, and relationships.

---

### 🔁 API Interaction Flow (Sequence Diagrams)

#### ✅ Register New User

```mermaid
sequenceDiagram
    participant User
    participant UserAPI
    participant HBnBFacade
    participant UserService
    participant UserRepository
    participant Database

    User->>UserAPI: POST /register (email, password, name)
    UserAPI->>HBnBFacade: register_user(data)
    HBnBFacade->>UserService: validate_and_create_user(data)
    UserService->>UserRepository: save_user_to_db()
    UserRepository->>Database: INSERT user record
    Database-->>UserRepository: confirmation
    UserRepository-->>UserService: success
    UserService-->>HBnBFacade: user_created
    HBnBFacade-->>UserAPI: return success
    UserAPI-->>User: 201 Created + user_id
```

### Explanation:

1. User submits registration.
2. Facade handles logic.
3. User is saved to DB.

---

#### ✅ Create New Place

```mermaid
sequenceDiagram
    participant User
    participant PlaceAPI
    participant HBnBFacade
    participant PlaceService
    participant PlaceRepository
    participant Database

    User->>PlaceAPI: POST /places (title, price, etc.)
    PlaceAPI->>HBnBFacade: create_place(data)
    HBnBFacade->>PlaceService: validate_and_create(data)
    PlaceService->>PlaceRepository: save_place()
    PlaceRepository->>Database: INSERT place
    Database-->>PlaceRepository: confirmation
    PlaceRepository-->>PlaceService: success
    PlaceService-->>HBnBFacade: place_created
    HBnBFacade-->>PlaceAPI: return success
    PlaceAPI-->>User: 201 Created + place_id
```

### Explanation:

1. User creates a place.
2. Data validated and stored.
3. Confirmation returned.

---

#### ❌ Review Submission Failed (Unauthorized)

```mermaid
sequenceDiagram
    participant User
    participant ReviewAPI
    participant HBnBFacade
    participant ReviewService
    participant BookingRepository

    User->>ReviewAPI: POST /places/:id/reviews (rating, comment)
    ReviewAPI->>HBnBFacade: submit_review(data)
    HBnBFacade->>ReviewService: validate_review(data)
    ReviewService->>BookingRepository: check_user_visit()
    BookingRepository-->>ReviewService: Not visited
    ReviewService-->>HBnBFacade: error (unauthorized)
    HBnBFacade-->>ReviewAPI: return 403
    ReviewAPI-->>User: 403 Forbidden
```

### Explanation:

1. User tries to submit a review.
2. System checks visit.
3. Returns 403 if not allowed.

---

#### ✅ Admin Deletes Place

```mermaid
sequenceDiagram
    participant Admin
    participant PlaceAPI
    participant HBnBFacade
    participant PlaceService
    participant PlaceRepository
    participant Database

    Admin->>PlaceAPI: DELETE /places/:id
    PlaceAPI->>HBnBFacade: delete_place(place_id)
    HBnBFacade->>PlaceService: check_admin_and_delete()
    alt is_admin
        PlaceService->>PlaceRepository: delete_place()
        PlaceRepository->>Database: DELETE FROM places
        Database-->>PlaceRepository: confirmation
        PlaceRepository-->>PlaceService: deleted
        PlaceService-->>HBnBFacade: success
        HBnBFacade-->>PlaceAPI: 200 OK
        PlaceAPI-->>Admin: Place deleted
    else not_admin
        PlaceService-->>HBnBFacade: 403 Forbidden
        HBnBFacade-->>PlaceAPI: error
        PlaceAPI-->>Admin: Access Denied
    end
```

### Explanation:

* If admin: place is deleted.
* If not admin: system denies access.

---

### ✅ API Call: Fetch List of Places

```mermaid
sequenceDiagram
    participant User
    participant PlaceAPI
    participant HBnBFacade
    participant PlaceService
    participant PlaceRepository
    participant Database

    User->>PlaceAPI: GET /places?location=city
    PlaceAPI->>HBnBFacade: fetch_places_by_location(city)
    HBnBFacade->>PlaceService: get_filtered_places(city)
    PlaceService->>PlaceRepository: query_places(city)
    PlaceRepository->>Database: SELECT * FROM places WHERE city=?
    Database-->>PlaceRepository: return results
    PlaceRepository-->>PlaceService: places list
    PlaceService-->>HBnBFacade: places list
    HBnBFacade-->>PlaceAPI: return results
    PlaceAPI-->>User: 200 OK + places
```

**Explanation:**
1. User requests places in a city.
2. The API forwards the query to the facade.
3. The business logic retrieves matching places from the DB.
4. Response is sent back to the user.

---

### 📝 API Call: Submit Review

```mermaid
sequenceDiagram
    participant User
    participant ReviewAPI
    participant HBnBFacade
    participant ReviewService
    participant ReviewRepository
    participant Database

    User->>ReviewAPI: POST /reviews (place_id, rating, comment)
    ReviewAPI->>HBnBFacade: submit_review(data)
    HBnBFacade->>ReviewService: validate_and_create_review(data)
    ReviewService->>ReviewRepository: save_review_to_db()
    ReviewRepository->>Database: INSERT review
    Database-->>ReviewRepository: confirmation
    ReviewRepository-->>ReviewService: saved
    ReviewService-->>HBnBFacade: review_created
    HBnBFacade-->>ReviewAPI: return success
    ReviewAPI-->>User: 201 Created + review_id
```

**Explanation:**
1. The user submits a review via the API.
2. The request goes through the business logic and gets saved.
3. Confirmation is returned to the user.

---

### ❌ API Call: Failed Registration (Invalid Input)

```mermaid
sequenceDiagram
    participant User
    participant UserAPI
    participant HBnBFacade
    participant UserService

    User->>UserAPI: POST /register (invalid email or missing password)
    UserAPI->>HBnBFacade: register_user(data)
    HBnBFacade->>UserService: validate_and_create_user(data)
    UserService-->>HBnBFacade: error ("Invalid input")
    HBnBFacade-->>UserAPI: return error
    UserAPI-->>User: 400 Bad Request + error message
```

**Explanation:**
1. Invalid data is sent to register.
2. Validation fails and error is returned.
3. User gets a 400 Bad Request response.
---

✅ End of Technical Document
