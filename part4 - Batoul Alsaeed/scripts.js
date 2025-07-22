document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://localhost:5000/api/v1/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`; // Store token in cookies
          window.location.href = 'index.html'; // Redirect to the home page
        } else {
          const error = await response.json();
          alert('Login failed: ' + (error.message || response.statusText));
        }

      } catch (err) {
        console.error('Error:', err);
        alert('Something went wrong. Please try again later.');
      }
    });
  }
});

// Global token variable to reuse across functions
let userToken = null;

/* Get token from cookies */
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

/* LOGIN: Handle login form submission */
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://localhost:5000/api/v1/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
          const data = await response.json();
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          const error = await response.json();
          alert('Login failed: ' + (error.message || response.statusText));
        }
      } catch (err) {
        console.error('Error:', err);
        alert('Something went wrong. Please try again later.');
      }
    });
  }
});

/* INDEX: Check user authentication */
function checkAuthentication() {
  userToken = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) {
    loginLink.style.display = userToken ? 'none' : 'block';
  }
  fetchPlaces(userToken);
}

/* INDEX: Fetch all places from API */
async function fetchPlaces(token) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/places', {
      method: 'GET',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
    });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
      setupPriceFilter(places);
    } else {
      alert('Failed to fetch places');
    }
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

/* INDEX: Display list of places */
function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.classList.add('place-card');
    card.setAttribute('data-price', place.price);

    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>$${place.price}/night</p>
      <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
    `;

    list.appendChild(card);
  });
}

/* INDEX: Setup price filtering */
function setupPriceFilter(places) {
  const filter = document.getElementById('price-filter');
  if (!filter) return;

  filter.innerHTML = `
    <option value="All">All</option>
    <option value="10">Under $10</option>
    <option value="50">Under $50</option>
    <option value="100">Under $100</option>
  `;

  filter.addEventListener('change', (event) => {
    const maxPrice = event.target.value;
    document.querySelectorAll('.place-card').forEach(card => {
      const price = parseFloat(card.getAttribute('data-price'));
      card.style.display = (maxPrice === 'All' || price <= parseFloat(maxPrice)) ? 'block' : 'none';
    });
  });
}

/* PLACE: Extract place ID from URL */
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

/* PLACE: Check user auth and fetch place details */
function checkPlaceAuthentication() {
  userToken = getCookie('token');
  const addReviewSection = document.getElementById('add-review');
  const placeId = getPlaceIdFromURL();

  if (addReviewSection) {
    addReviewSection.style.display = userToken ? 'block' : 'none';
  }

  fetchPlaceDetails(userToken, placeId);
}

/* PLACE: Fetch specific place details */
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
    });

    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    } else {
      alert('Failed to fetch place details');
    }
  } catch (error) {
    console.error('Error fetching place:', error);
  }
}

/* PLACE: Display place details and reviews */
function displayPlaceDetails(place) {
  const section = document.getElementById('place-details');
  if (!section) return;
  section.innerHTML = '';

  const container = document.createElement('div');
  container.classList.add('place-info');
  container.innerHTML = `
    <h2>${place.name}</h2>
    <p><strong>Host:</strong> ${place.host}</p>
    <p><strong>Price:</strong> $${place.price}/night</p>
    <p><strong>Description:</strong> ${place.description}</p>
    <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
  `;
  section.appendChild(container);

  const reviewsSection = document.getElementById('reviews');
  if (!reviewsSection) return;
  reviewsSection.innerHTML = '<h3>Reviews</h3>';
  place.reviews.forEach(review => {
    const reviewCard = document.createElement('div');
    reviewCard.classList.add('review-card');
    reviewCard.innerHTML = `
      <p><strong>${review.user}:</strong> ${review.comment}</p>
      <p>Rating: ${'⭐'.repeat(review.rating)}</p>
    `;
    reviewsSection.appendChild(reviewCard);
  });
}

/* Global initializer */
document.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname.includes('index.html')) {
    checkAuthentication();
  }

  if (window.location.pathname.includes('place.html')) {
    checkPlaceAuthentication();
  }
});
