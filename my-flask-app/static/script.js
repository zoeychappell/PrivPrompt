// script.js
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("promptInput");
    const button = document.getElementById("submitBtn");
    const llmSelector = document.getElementById("llmSelector");

    const originalBox = document.getElementById("originalPrompt");
    const sanitizedBox = document.getElementById("sanitizedPrompt");
    const detectedBox = document.getElementById("detected");
    const aiResponseSanitized = document.getElementById("aiResponseSanitized"); // Only this exists in HTML

    const apiBase = `${window.location.protocol}//${window.location.hostname}:5001`;

    function setLoading(element) {
        element.innerHTML = '<div class="loading">Processing...</div>';
    }

    function setPlaceholder(element, text) {
        element.textContent = text;
        element.style.color = '#666';
        element.style.fontStyle = 'italic';
    }

    function clearStyles(element) {
        element.style.color = '';
        element.style.fontStyle = '';
    }

    // Set initial placeholders - REMOVED aiResponseOriginal since it doesn't exist in HTML
    setPlaceholder(detectedBox, "No sensitive information detected yet...");
    setPlaceholder(sanitizedBox, "Sanitized version will appear here...");
    setPlaceholder(aiResponseSanitized, "AI response using sanitized prompt...");

    button.addEventListener("click", async () => {
        const prompt = input.value.trim();
        const selectedLLM = llmSelector.value;

        if (!prompt) {
            alert("Please enter a prompt before submitting.");
            return;
        }

        // Clear previous results and set loading
        setLoading(sanitizedBox);
        setLoading(detectedBox);
        setLoading(aiResponseSanitized);

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
            if (data.result) {
                sanitizedBox.textContent = data.result;
                clearStyles(sanitizedBox);
            } else {
                setPlaceholder(sanitizedBox, "No sanitized prompt returned.");
            }
            
            // Update detected info
            if (data.detected) {
                const { emails, ssns, names, phones, dates } = data.detected;
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
                if (Object.keys(dates).length > 0) {
                    sections.push("Dates: " + Object.keys(dates).join(", "));
                }
                
                if (sections.length > 0) {
                    detectedBox.textContent = sections.join("\n");
                    clearStyles(detectedBox);
                } else {
                    setPlaceholder(detectedBox, "No sensitive information detected.");
                }
            } else {
                setPlaceholder(detectedBox, "No sensitive information detected.");
            }

            // Update AI response - ONLY the sanitized one (original doesn't exist in HTML)
            if (data.ai_sanitized) {
                aiResponseSanitized.textContent = data.ai_sanitized;
                clearStyles(aiResponseSanitized);
            } else {
                setPlaceholder(aiResponseSanitized, "No response received.");
            }

        } catch (err) {
            console.error("Error:", err);
            sanitizedBox.textContent = "Error: " + err.message;
            detectedBox.textContent = "Error processing request";
            aiResponseSanitized.textContent = "Error getting response";
            
            // Style error messages
            [sanitizedBox, detectedBox, aiResponseSanitized].forEach(box => {
                box.style.color = '#dc3545';
                box.style.fontStyle = 'normal';
            });
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