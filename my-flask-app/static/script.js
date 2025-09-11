document.addEventListener("DOMContentLoaded", () => {
  // Grab references to HTML elements by their IDs
  const input = document.getElementById("promptInput");   // Text input field
  const button = document.getElementById("submitBtn");    // Submit button
  const results = document.getElementById("results");     // Results display area

  // Dynamically build API URL based on current host (localhost:5000, 5001, etc.)
  // Ensures it works whether served on localhost, 127.0.0.1, or another host
  const apiBase = `${window.location.protocol}//${window.location.hostname}:5001`;

  // Add a click event listener to the submit button
  button.addEventListener("click", async () => {
    const prompt = input.value.trim(); // Get the input value and remove whitespace

    // If no input is provided, show an error message and stop
    if (!prompt) {
      results.textContent = "Please enter a prompt."; 
      return;
    }

    // Show loading text while waiting for a server response
    results.textContent = "Loading...";

    try {
      // Send the prompt to the backend API using a POST request
      const response = await fetch(`${apiBase}/api/prompt`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }, // Tell server we're sending JSON
        body: JSON.stringify({ prompt }), // Send the prompt as JSON in the request body
      });

      // If server responds with an error status, throw an exception
      if (!response.ok) {
        throw new Error("Server error: " + response.status);
      }

      // Parse JSON response from the server
      const data = await response.json();

      // Display the result text returned by the server (or fallback message)
      results.textContent = data.result || "No response from server.";

    } catch (err) {
      results.textContent = "Error: " + err.message;
    }
  });
});
