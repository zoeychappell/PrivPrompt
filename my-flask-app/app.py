from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from livereload import Server
from sanitize import sanitize_input

# --- IMPORT ALL LLM CLIENTS ---
from llm_clients.groq_llm_client import call_groq
from llm_clients.cohere_llm_client import cohere
from llm_clients.google_genai_llm_client import call_genai
from llm_clients.deepseek_llm_client import call_deepseek
from llm_clients.workers_ai_llm_client import call_workers_ai

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # disable caching
CORS(app)

# --- HELPER FUNCTION TO ROUTE LLM CALLS ---
def call_llm(prompt, llm_name):
    """Calls the selected LLM based on the llm_name."""
    if llm_name == "cohere":
        return cohere(prompt)
    elif llm_name == "gemini":
        return call_genai(prompt)
    elif llm_name == "deepseek":
        return call_deepseek(prompt)
    elif llm_name == "workers_ai":
        return call_workers_ai(prompt)
    elif llm_name == "llama":
        # Default to llama (Groq)
        return call_groq(prompt)
    else:
        # Fallback default
        return call_groq(prompt)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    # --- GET THE CHOSEN LLM FROM THE REQUEST ---
    llm_choice = data.get("llm", "llama") # Default to 'llama' if not provided

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # --- CALL SANITIZE_INPUT WITH interactive=False TO SKIP CLI PROMPTS ---
    # sanitize_input returns 7 values now
    sanitized_prompt, _, dict_email, dict_ssn, dict_name, dict_phone, dict_dates = sanitize_input(prompt, interactive=False)

    # Get only the sanitized response (skip original for efficiency)
    ai_response_sanitized = call_llm(sanitized_prompt, llm_choice)

    # --- RETURN JSON RESPONSE ---
    return jsonify({
        "result": sanitized_prompt,
        "detected": {
            "emails": dict_email,
            "ssns": dict_ssn,
            "names": dict_name,
            "phones": dict_phone,
            "dates": dict_dates
        },
        "ai_sanitized": ai_response_sanitized  # Only send sanitized response
    })


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch('templates/*')
    server.watch('static/*')
    server.serve(port=5001, debug=True)