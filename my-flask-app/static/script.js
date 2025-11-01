document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("promptInput");
  const button = document.getElementById("submitBtn");
  
  // --- 1. GET THE NEW LLM SELECTOR ---
  const llmSelector = document.getElementById("llmSelector");

  const originalBox = document.getElementById("originalPrompt");
  const sanitizedBox = document.getElementById("sanitizedPrompt");
  const detectedBox = document.getElementById("detected");
  const aiResponseOriginal = document.getElementById("aiResponseOriginal");
  const aiResponseSanitized = document.getElementById("aiResponseSanitized");

  const apiBase = `${window.location.protocol}//${window.location.hostname}:5001`;

  button.addEventListener("click", async () => {
    const prompt = input.value.trim();
    
    // --- 2. GET THE SELECTED LLM'S VALUE ---
    const selectedLLM = llmSelector.value;

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
        // --- 3. SEND BOTH PROMPT AND LLM CHOICE ---
        body: JSON.stringify({ prompt: prompt, llm: selectedLLM }),
      });

      if (!response.ok) throw new Error("Server error: " + response.status);

      const data = await response.json();

      // Update sanitized prompt
      sanitizedBox.textContent = data.result || "No sanitized prompt returned.";

      // --- 4. UPDATE DETECTED INFO (WITH PHONES) ---
      let detectedText = "";
      if (data.detected) {
        // Destructure phones from the response
        const { emails, ssns, names, phones } = data.detected;
        if (Object.keys(names).length > 0) {
          detectedText += "Names: " + Object.keys(names).join(", ") + "\n";
        }
        if (Object.keys(emails).length > 0) {
          detectedText += "Emails: " + Object.keys(emails).join(", ") + "\n";
        }
        if (Object.keys(ssns).length > 0) {
          detectedText += "SSNs: " + Object.keys(ssns).join(", ") + "\n";
        }
        // Add new block for phones
        if (Object.keys(phones).length > 0) {
          detectedText += "Phones: " + Object.keys(phones).join(", ");
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