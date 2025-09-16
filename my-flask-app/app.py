from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from livereload import Server
from sanitize import sanitize_input  # import your sanitization functions

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # no caching
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Use your sanitization function
    sanitized_prompt, emails_found, ssns_found = sanitize_input(prompt)

    # Example: AI processing could go here (for now, just echo sanitized)
    ai_response = f"Sanitized Prompt: {sanitized_prompt}"

    # Return both the sanitized result and what was detected
    return jsonify({
        "result": ai_response,
        "detected": {
            "emails": emails_found,
            "ssns": ssns_found
        }
    })

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch('templates/*')
    server.watch('static/*')
    server.serve(port=5001, debug=True)
