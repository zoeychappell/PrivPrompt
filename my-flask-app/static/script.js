document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("promptInput");
  const button = document.getElementById("submitBtn");
  const results = document.getElementById("results");

  // Dynamically build API URL based on current host (localhost:5000, 5001, etc.)
  const apiBase = `${window.location.protocol}//${window.location.hostname}:5001`;

  button.addEventListener("click", async () => {
    const prompt = input.value.trim();
    if (!prompt) {
      results.textContent = "Please enter a prompt.";
      return;
    }

    results.textContent = "Loading...";

    try {
      const response = await fetch(`${apiBase}/api/prompt`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error("Server error: " + response.status);
      }

      const data = await response.json();
      results.textContent = data.result || "No response from server.";
    } catch (err) {
      results.textContent = "Error: " + err.message;
    }
  });
});
