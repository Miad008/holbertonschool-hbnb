document.addEventListener('DOMContentLoaded', () => {
  // Login form submission handler (Task 1)
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

  // Task 2: Check authentication and show/hide login link
  function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (!token) {
      if (loginLink) loginLink.style.display = 'block';
    } else {
      if (loginLink) loginLink.style.display = 'none';
      fetchPlaces(token);
    }
  }

  // Task 2: Fetch places data from API
  async function fetchPlaces(token) {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Failed to fetch places');
      const places = await response.json();
      displayPlaces(places);
    } catch (error) {
      console.error('Error fetching places:', error);
    }
  }

  // Task 2: Display places on the page
  function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    placesList.innerHTML = '';
    places.forEach(place => {
      const placeDiv = document.createElement('div');
      placeDiv.className = 'place-card';
      placeDiv.dataset.price = place.price;
      placeDiv.innerHTML = `
        <h3>${place.name}</h3>
        <p>${place.description || ''}</p>
        <p><strong>Price:</strong> $${place.price}/night</p>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
      `;
      placesList.appendChild(placeDiv);
    });
  }

  // Task 2: Price filter dropdown setup and event listener
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

  // Call checkAuthentication on page load
  checkAuthentication();
});

// Utility function to get cookie value by name
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split('=');
    if (cookieName === name) return cookieValue;
  }
  return null;
}
