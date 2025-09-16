document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("promptInput");
  const button = document.getElementById("submitBtn");
  const originalBox = document.getElementById("originalPrompt");
  const sanitizedBox = document.getElementById("sanitizedPrompt");
  const detectedBox = document.getElementById("detected");

  const apiBase = `${window.location.protocol}//${window.location.hostname}:5001`;

  button.addEventListener("click", async () => {
    const prompt = input.value.trim();

    if (!prompt) {
      originalBox.textContent = "";
      sanitizedBox.textContent = "";
      detectedBox.textContent = "";
      return;
    }

    originalBox.textContent = prompt;
    sanitizedBox.textContent = "Loading...";
    detectedBox.textContent = "";

    try {
      const response = await fetch(`${apiBase}/api/prompt`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) throw new Error("Server error: " + response.status);

      const data = await response.json();

      sanitizedBox.textContent = data.result || "No sanitized prompt returned.";

      let detectedText = "";
      if (data.detected) {
        const { emails, ssns } = data.detected;
        if (Object.keys(emails).length > 0)
          detectedText += "Emails: " + Object.keys(emails).join(", ") + "\n";
        if (Object.keys(ssns).length > 0)
          detectedText += "SSNs: " + Object.keys(ssns).join(", ");
      }
      detectedBox.textContent = detectedText || "No sensitive info detected.";

    } catch (err) {
      sanitizedBox.textContent = "Error: " + err.message;
      detectedBox.textContent = "";
    }
  });
});
