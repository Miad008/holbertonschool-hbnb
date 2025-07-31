document.addEventListener('DOMContentLoaded', () => {

  // Task 1: Handle login
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = loginForm.email.value;
      const password = loginForm.password.value;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });
        if (response.ok) {
          const data = await response.json();
          if (data.access_token) {
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
          } else {
            alert('Login failed: Invalid credentials');
          }
        } else {
          const errorData = await response.json();
          alert('Login failed: ' + (errorData.message || response.statusText));
        }
      } catch (error) {
        alert('Login failed: Network error');
        console.error(error);
      }
    });
  }

  // Task 2: Price filter
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.innerHTML = `
      <option value="all">All</option>
      <option value="10">Under $10</option>
      <option value="50">Under $50</option>
      <option value="100">Under $100</option>
    `;

    priceFilter.addEventListener('change', (event) => {
      const maxPrice = event.target.value;
      const places = document.querySelectorAll('.place-card');
      places.forEach(place => {
        const price = parseFloat(place.dataset.price);
        if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
          place.style.display = 'block';
        } else {
          place.style.display = 'none';
        }
      });
    });
  }

  // Task 3: Check auth & fetch data
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'block';
  }

  const placeId = getPlaceIdFromURL();

  if (placeId) {
    fetchPlaceDetails(token, placeId);
    handleReviewForm(token, placeId);
  } else {
    fetchPlaces(token);
  }
});

// Task 3: Get token from cookies
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split('=');
    if (cookieName === name) return cookieValue;
  }
  return null;
}

// Task 3: Get place ID from URL
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// Task 3: Fetch all places
async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
      method: 'GET',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error('Failed to fetch places');
    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

// Task 3: Display places on home page
function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';
  places.forEach(place => {
    const div = document.createElement('div');
    div.className = 'place-card';
    div.dataset.price = place.price;
    div.innerHTML = `
      <h3>${place.name}</h3>
      <p>${place.description || ''}</p>
      <p><strong>Price:</strong> $${place.price}/night</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;
    list.appendChild(div);
  });
}

// Task 3: Fetch place details
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error('Failed to fetch place details');
    const place = await response.json();
    displayPlaceDetails(place);
    displayReviews(place.reviews || []);
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

// Task 3: Display place details
function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;
  container.innerHTML = `
    <h2>${place.title}</h2>
    <p><strong>Host:</strong> ${place.owner?.first_name || ''} ${place.owner?.last_name || ''}</p>
    <p><strong>Price:</strong> $${place.price}/night</p>
    <p><strong>Description:</strong> ${place.description}</p>
    <p><strong>Amenities:</strong> ${place.amenities?.map(a => a.name).join(', ') || 'None'}</p>
  `;
}

// Task 3: Display reviews
function displayReviews(reviews) {
  const reviewsContainer = document.getElementById('reviews');
  if (!reviewsContainer) return;
  reviewsContainer.innerHTML = '<h2>Reviews</h2>';
  if (reviews.length === 0) {
    reviewsContainer.innerHTML += '<p>No reviews yet.</p>';
    return;
  }
  reviews.forEach(review => {
    const div = document.createElement('div');
    div.className = 'review-card';
    const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
    div.innerHTML = `
      <p><strong>${review.user?.first_name || 'Anonymous'}:</strong> ${review.text}</p>
      <p>Rating: ${stars}</p>
    `;
    reviewsContainer.appendChild(div);
  });
}

// Task 3: Handle review submission
function handleReviewForm(token, placeId) {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm || !token || !placeId) return;

  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const review = document.getElementById('review').value || document.getElementById('review-text').value;
    const rating = document.getElementById('rating').value;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const userId = payload.sub;

      const res = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          text: review,
          rating: parseInt(rating),
          user_id: userId,
          place_id: placeId
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || 'Unknown error');
      }

      alert('Review submitted successfully!');
      reviewForm.reset();
      fetchPlaceDetails(token, placeId);
    } catch (error) {
      console.error('Error submitting review:', error);
      alert('Failed to submit review: ' + error.message);
    }
  });
}
