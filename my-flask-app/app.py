from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__) # Create a Flask application instance
CORS(app) # Enable CORS for the app so frontend JS can make API calls

# Serve index.html at the root ("/") route
@app.route("/")
def home():
    return render_template("index.html") # Render the template "index.html"

# API endpoint that handles POST requests to /api/prompt
@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    data = request.get_json() # Parse incoming JSON data from the request
    prompt = data.get("prompt", "") # Get the "prompt" field or default to empty
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    return jsonify({"result": f"You entered: {prompt}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) # Start server on port 5001 with debug enabled
