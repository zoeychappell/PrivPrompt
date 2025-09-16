const input = document.getElementById("promptInput");
const button = document.getElementById("submitBtn");
const results = document.getElementById("results");
const detected = document.getElementById("detected");

button.addEventListener("click", async () => {
    const prompt = input.value.trim();
    if (!prompt) {
        results.textContent = "Please enter a prompt.";
        detected.textContent = "";
        return;
    }

    results.textContent = "Loading...";
    detected.textContent = "";

    try {
        const response = await fetch("/api/prompt", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt }),
        });

        const data = await response.json();

        if (data.error) {
            results.textContent = data.error;
            return;
        }

        results.textContent = data.result;

        // Display detected sensitive info
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
        detected.textContent = detectedText || "No sensitive info detected.";

    } catch (err) {
        results.textContent = "Error: " + err.message;
    }
});
