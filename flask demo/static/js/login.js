const form = document.getElementById("login-form");
form.addEventListener("submit", handleFormSubmit);

function handleFormSubmit(event) {
  event.preventDefault(); // Prevent form submission

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  // Validate input
  if (username === "" || password === "") {
    alert("Please fill in all fields.");
    return;
  }

  // Send data to server for further processing
  fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: username, password: password })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      window.location.href = "/";
    } else {
      alert(data.message);
    }
  })
  .catch(error => {
    console.error("Error:", error);
  });

  // Clear form fields
  form.reset();
}
