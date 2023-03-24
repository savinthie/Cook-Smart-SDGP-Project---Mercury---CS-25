const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", handleFormSubmit);

function handleFormSubmit(event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  // Validate input
  if (username === "" || password === "") {
    alert("Please fill in all fields.");
    return;
  }
  

  // Send data to server for authentication
  fetch('/submit_login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, password })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Login successful, redirect to home page or show success message
      window.location.href = "/home";
    } else {
      // Login failed, show error message
      const errorDiv = document.getElementById("error-message");
      errorDiv.innerHTML = "Incorrect username or password.";
    }
  })
  .catch(error => console.error(error));

  // Clear form fields
  loginForm.reset();
}

