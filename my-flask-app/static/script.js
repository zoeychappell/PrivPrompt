document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("promptInput");
  const button = document.getElementById("submitBtn");

  const originalBox = document.getElementById("originalPrompt");
  const sanitizedBox = document.getElementById("sanitizedPrompt");
  const detectedBox = document.getElementById("detected");
  const aiResponseOriginal = document.getElementById("aiResponseOriginal");
  const aiResponseSanitized = document.getElementById("aiResponseSanitized");

  const apiBase = `${window.location.protocol}//${window.location.hostname}:5001`;

  button.addEventListener("click", async () => {
    const prompt = input.value.trim();

    if (!prompt) {
      originalBox.textContent = "";
      sanitizedBox.textContent = "";
      detectedBox.textContent = "";
      aiResponseOriginal.textContent = "";
      aiResponseSanitized.textContent = "";
      return;
    }

    // Set loading states
    originalBox.textContent = prompt;
    sanitizedBox.textContent = "Loading...";
    detectedBox.textContent = "";
    aiResponseOriginal.textContent = "Loading...";
    aiResponseSanitized.textContent = "Loading...";

    try {
      const response = await fetch(`${apiBase}/api/prompt`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) throw new Error("Server error: " + response.status);

      const data = await response.json();

      // Update sanitized prompt
      sanitizedBox.textContent = data.result || "No sanitized prompt returned.";

      // Update detected sensitive info
      let detectedText = "";
      if (data.detected) {
        const { emails, ssns } = data.detected;
        if (Object.keys(emails).length > 0) {
          detectedText += "Emails: " + Object.keys(emails).join(", ") + "\n";
        }
        if (Object.keys(ssns).length > 0) {
          detectedText += "SSNs: " + Object.keys(ssns).join(", ");
        }
      }
      detectedBox.textContent = detectedText || "No sensitive info detected.";

      // Update AI responses
      aiResponseOriginal.textContent = data.ai_original || "No response.";
      aiResponseSanitized.textContent = data.ai_sanitized || "No response.";
    } catch (err) {
      sanitizedBox.textContent = "Error: " + err.message;
      detectedBox.textContent = "";
      aiResponseOriginal.textContent = "";
      aiResponseSanitized.textContent = "";
    }
  });
});
