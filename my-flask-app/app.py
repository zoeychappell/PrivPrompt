from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from livereload import Server
from sanitize import sanitize_input
from groq_llm_client import groq

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # disable caching
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Sanitize
    sanitized_prompt, dict_email, dict_ssn = sanitize_input(prompt)

    # AI calls
    ai_response_original = groq(prompt)
    ai_response_sanitized = groq(sanitized_prompt)

    return jsonify({
        "result": sanitized_prompt,
        "detected": {
            "emails": dict_email,
            "ssns": dict_ssn
        },
        "ai_original": ai_response_original,
        "ai_sanitized": ai_response_sanitized
    })

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch('templates/*')
    server.watch('static/*')
    server.serve(port=5001, debug=True)
