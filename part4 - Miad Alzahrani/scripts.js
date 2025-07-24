document.addEventListener('DOMContentLoaded', () => {
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
});

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split('=');
    if (cookieName === name) return cookieValue;
  }
  return null;
}

