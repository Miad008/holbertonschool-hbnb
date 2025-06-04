## 🔁 API Call: Review Submission – Success or Fail

This diagram handles both successful and failed review submissions depending on whether the user visited the place.

```mermaid
sequenceDiagram
    participant  User
    participant  ReviewAPI
    participant  HBnBFacade
    participant  ReviewService
    participant  BookingRepository
    participant  ReviewRepository

    User->>ReviewAPI: POST /places/:id/review (rating, comment)
    ReviewAPI->>HBnBFacade: submit_review(data)
    HBnBFacade->>ReviewService: validate_and_create_review(data)
    ReviewService->>BookingRepository: check_if_user_visited_place(user_id, place_id)
    alt  User has visited
        ReviewService->>ReviewRepository: save_review()
        ReviewRepository-->>ReviewService: success
        ReviewService-->>HBnBFacade: review_created
        HBnBFacade-->>ReviewAPI: return success
        ReviewAPI-->>User: 201 Created + review_id
    else  User has NOT visited
        ReviewService-->>HBnBFacade: error ("User has not visited")
        HBnBFacade-->>ReviewAPI: return error
        ReviewAPI-->>User: 403 Forbidden + message
    end
```

### Explanation:
1. The **User** submits a review for a specific place.
2. The **ReviewAPI** sends the request to the **HBnBFacade**, which forwards it to **ReviewService**.
3. The **ReviewService** checks with **BookingRepository** whether the user has visited the place.
4. If visited:
   - The review is saved via **ReviewRepository**.
   - A success response is returned with `201 Created` and the review ID.
5. If not visited:
   - The system returns a `403 Forbidden` error, informing the user they can't review the place.
