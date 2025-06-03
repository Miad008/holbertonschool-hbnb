## API Call: Register New User

This sequence diagram illustrates how a new user registration request is processed through the system layers in HBnB.

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


### Explanation:
```mermaid
1. **User** submits registration info via API.
2. **UserAPI** forwards the request to the **Facade** layer.
3. **HBnBFacade** delegates it to **UserService**, which handles logic.
4. **UserService** saves the data through **UserRepository** into the **Database**.
5. The confirmation is sent back through the layers to the user.
