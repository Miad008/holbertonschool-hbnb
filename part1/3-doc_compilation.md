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

#### 1.Register New User

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
- **Purpose**: Allows a new user to create an account.

### Explanation:

1. User submits registration.
2. Facade handles logic.
3. User is saved to DB.

---

#### 2.Create New Place

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
- **Purpose**: Allows a user to list a new property.

### Explanation:

1. User creates a place.
2. Data validated and stored.
3. Confirmation returned.

---

### 3.Submit Review

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
- **Purpose**: Enables users to submit a review for a place.

**Explanation:**
1. The user submits a review via the API.
2. The request goes through the business logic and gets saved.
3. Confirmation is returned to the user.

---

### 4. Get List of Places  

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
- **Purpose**: Retrieve a list of available places.

**Explanation:**
1. User requests places in a city.
2. The API forwards the query to the facade.
3. The business logic retrieves matching places from the DB.
4. Response is sent back to the user.

---

## 🧩 Additional Sequence Diagrams (Optional but valuable)

### 5. Create Amenity  

```mermaid
sequenceDiagram
    participant Admin
    participant AmenityAPI
    participant HBnBFacade
    participant AmenityService
    participant AmenityRepository
    participant Database

    Admin->>AmenityAPI: POST /amenities (name, description)
    AmenityAPI->>HBnBFacade: create_amenity(data)
    HBnBFacade->>AmenityService: validate_and_create(data)
    AmenityService->>AmenityRepository: save_to_db(data)
    AmenityRepository->>Database: INSERT INTO amenities
    Database-->>AmenityRepository: amenity_created
    AmenityRepository-->>AmenityService: success
    AmenityService-->>HBnBFacade: amenity_created
    HBnBFacade-->>AmenityAPI: return 201 Created
    AmenityAPI-->>Admin: Amenity Created
```
- **Purpose**: Admin can add a new amenity (e.g., Wi-Fi).

#### 6.Review Submission Failed (Unauthorized)

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
- **Purpose**: Shows possible outcomes (success or 403 forbidden).

### Explanation:

1. User tries to submit a review.
2. System checks visit.
3. Returns 403 if not allowed.

---

### 7.Failed Registration (Invalid Input)

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
- **Purpose**: Shows what happens when user registration fails.

**Explanation:**
1. Invalid data is sent to register.
2. Validation fails and error is returned.
3. User gets a 400 Bad Request response.

---

#### 8.Admin Deletes Place

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
- **Purpose**: Admin deletes a place listing.

### Explanation:

* If admin: place is deleted.
* If not admin: system denies access.

---

---

## ✅ Final Summary

This document summarizes the technical design and architecture of the HBnB Evolution project, completed as part of our training with **Holberton School – Tuwaiq Academy**.

It includes high-level architecture, detailed class structure, and API interaction flows, covering all core components of the system.

> Prepared with the collaboration of team members: **Batoul Alsaeed**, **Miad Alzhrani**, and **Rawan Albaraiki**.

This documentation is intended to guide the implementation phases and serve as a reference throughout the development process.
