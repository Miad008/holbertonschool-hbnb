## API Call: Register New User

This sequence diagram illustrates how a new user registration request is processed through the system layers in HBnB.

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
