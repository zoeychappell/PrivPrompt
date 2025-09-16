from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from livereload import Server  # 👈 import LiveReload

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # no caching
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
    return jsonify({"result": f"You entered: {prompt}"})


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    # Watch files in templates/ and static/ for changes
    server.watch('templates/*')
    server.watch('static/*')
    # Start server on port 5001
    server.serve(port=5001, debug=True)
