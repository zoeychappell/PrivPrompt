// script.js
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("promptInput");
    const button = document.getElementById("submitBtn");
    const llmSelector = document.getElementById("llmSelector");

    const originalBox = document.getElementById("originalPrompt");
    const sanitizedBox = document.getElementById("sanitizedPrompt");
    const detectedBox = document.getElementById("detected");
    const aiResponseOriginal = document.getElementById("aiResponseOriginal");
    const aiResponseSanitized = document.getElementById("aiResponseSanitized");

    const apiBase = `${window.location.protocol}//${window.location.hostname}:5001`;

    function setLoading(element) {
        element.innerHTML = '<div class="loading">Processing...</div>';
    }

    function clearContent(element) {
        element.textContent = '';
    }

    button.addEventListener("click", async () => {
        const prompt = input.value.trim();
        const selectedLLM = llmSelector.value;

        if (!prompt) {
            alert("Please enter a prompt before submitting.");
            return;
        }

        // Clear previous results
        clearContent(originalBox);
        clearContent(sanitizedBox);
        clearContent(detectedBox);
        clearContent(aiResponseOriginal);
        clearContent(aiResponseSanitized);

        // Set loading states
        setLoading(sanitizedBox);
        setLoading(detectedBox);
        setLoading(aiResponseOriginal);
        setLoading(aiResponseSanitized);

        // Show original prompt immediately
        originalBox.textContent = prompt;

        try {
            console.log("Sending request to:", `${apiBase}/api/prompt`);
            const response = await fetch(`${apiBase}/api/prompt`, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ 
                    prompt: prompt, 
                    llm: selectedLLM 
                }),
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            console.log("Received data:", data);

            // Update all fields with the response data
            sanitizedBox.textContent = data.result || "No sanitized prompt returned.";
            
            // Update detected info
            if (data.detected) {
                const { emails, ssns, names, phones } = data.detected;
                const sections = [];
                
                if (Object.keys(names).length > 0) {
                    sections.push("Names: " + Object.keys(names).join(", "));
                }
                if (Object.keys(emails).length > 0) {
                    sections.push("Emails: " + Object.keys(emails).join(", "));
                }
                if (Object.keys(ssns).length > 0) {
                    sections.push("SSNs: " + Object.keys(ssns).join(", "));
                }
                if (Object.keys(phones).length > 0) {
                    sections.push("Phones: " + Object.keys(phones).join(", "));
                }
                
                detectedBox.textContent = sections.join("\n") || "No sensitive information detected.";
            } else {
                detectedBox.textContent = "No sensitive information detected.";
            }

            // Update AI responses
            aiResponseOriginal.textContent = data.ai_original || "No response received.";
            aiResponseSanitized.textContent = data.ai_sanitized || "No response received.";

        } catch (err) {
            console.error("Error:", err);
            sanitizedBox.textContent = "Error: " + err.message;
            detectedBox.textContent = "Error processing request";
            aiResponseOriginal.textContent = "Error getting response";
            aiResponseSanitized.textContent = "Error getting response";
        }
    });

    // Enter key support
    input.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
            button.click();
        }
    });

    // Auto-resize textarea
    input.addEventListener("input", function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 200) + 'px';
    });
});