const form = document.getElementById("signup-form");
form.addEventListener("submit", handleFormSubmit);

function handleFormSubmit(event) {
  event.preventDefault(); 

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  // Validate input
  if (username === "" || email === "" || password === "") {
    alert("Please fill in all fields.");
    return;
  }

  // Send data to server for further processing
  fetch('/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({username, email, password})
  })
  .then(response => {
    if (response.ok) {
      return response.text();
    } else if (response.status === 409) {
      alert("Username or email already taken.")
      throw new Error("Username or email already taken.");
     
    } else {
      alert("Something went wrong.")
      throw new Error("Something went wrong.");
    }
  })
  //.then(response => response.text())
  
  
  .then(data => {
    console.log(data);
    window.location.href = '/home';
  })
  .catch(error => console.error(error));
  

  // Clear form fields
  form.reset();
}
