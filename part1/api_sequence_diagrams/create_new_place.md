## API Call: Create New Place

This sequence diagram shows how a user creates a new place listing in the HBnB application, from the initial API request down to database storage.

```mermaid
sequenceDiagram
    participant User
    participant PlaceAPI
    participant HBnBFacade
    participant PlaceService
    participant PlaceRepository
    participant Database

    User->>PlaceAPI: POST /places (name, desc, price, location)
    PlaceAPI->>HBnBFacade: create_place(data)
    HBnBFacade->>PlaceService: validate_and_create_place(data)
    PlaceService->>PlaceRepository: save_place_to_db()
    PlaceRepository->>Database: INSERT place record
    Database-->>PlaceRepository: place_created
    PlaceRepository-->>PlaceService: success
    PlaceService-->>HBnBFacade: place_created
    HBnBFacade-->>PlaceAPI: return success
    PlaceAPI-->>User: 201 Created + place_id
```

### Explanation:

1. **User** submits a request to create a new place via the API.
2. **PlaceAPI** sends the data to the **HBnBFacade**, which acts as a bridge to the business logic.
3. **HBnBFacade** forwards the data to **PlaceService**, responsible for validation and creation logic.
4. **PlaceService** uses **PlaceRepository** to save the place into the **Database**.
5. Once the database confirms, the success message travels back up to the user with the new place ID.
