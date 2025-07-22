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
