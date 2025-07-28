
document.addEventListener("DOMContentLoaded", () => {
  const page = window.location.pathname;

  if (page.includes("login.html")) {
    const loginForm = document.getElementById("login-form");
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = loginForm.email.value;
      const password = loginForm.password.value;

      try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok && data.access_token) {
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = "index.html";
        } else {
          alert(data.error || "Login failed");
        }

      } catch (error) {
        console.error(error);
        alert("An error occurred during login");
      }

    });
  }
});
  else if (page.includes("index.html")) {
    const token = getCookie("token");
    const loginLink = document.getElementById("login-link");
    if (token && loginLink) loginLink.style.display = "none";

    const fetchPlaces = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/places");
        const places = await response.json();
        const placesList = document.getElementById("places-list");
        placesList.innerHTML = '';
        if (places.length === 0) {
          placesList.innerHTML = "<p>No places found.</p>";
        } else {
          places.forEach((place) => {
            const placeCard = createPlaceCard(place);
            placesList.appendChild(placeCard);
          });
        }
      } catch (error) {
        console.error(error);
      }
    };

    fetchPlaces();
  }

  else if (page.includes("place.html")) {
    const token = getCookie("token");
    const reviewSection = document.getElementById("review-section");
    if (!token && reviewSection) reviewSection.style.display = "none";

    const fetchPlaceDetails = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const placeId = urlParams.get("id");
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`);
        const place = await response.json();
        document.getElementById("place-name").textContent = place.name;
        document.getElementById("place-description").textContent = place.description;

        const reviewsList = document.getElementById("reviews-list");
        place.reviews.forEach((review) => {
          const li = document.createElement("li");
          li.textContent = `${review.user.first_name}: ${review.text}`;
          reviewsList.appendChild(li);
        });
      } catch (error) {
        console.error(error);
      }
    };

    fetchPlaceDetails();
  }

  else if (page.includes("add_review.html")) {
    const token = getCookie("token");
    if (!token) {
      window.location.href = "index.html";
      return;
    }

    const reviewForm = document.getElementById("review-form");
    reviewForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const review = document.getElementById("review").value;
      const rating = document.getElementById("rating").value;
      const urlParams = new URLSearchParams(window.location.search);
      const placeId = urlParams.get("id");

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ text: review, rating }),
        });
        if (response.ok) {
          alert("Review added successfully!");
          reviewForm.reset();
        } else {
          alert("Failed to add review.");
        }
      } catch (error) {
        console.error(error);
      }
    });
  }
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function createPlaceCard(place) {
  const div = document.createElement("div");
  div.className = "place-card";
  div.innerHTML = `
    <h3>${place.name}</h3>
    <p>${place.description}</p>
    <a href="place.html?id=${place.id}">View Details</a>
  `;
  return div;
}
