from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from livereload import Server
from sanitize import sanitize_input
from llm_clients.groq_llm_client import call_groq
# import json

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
    sanitized_prompt, dict_email, dict_ssn, dict_name = sanitize_input(prompt)

    # AI calls
    ai_response_original = call_groq(prompt)
    ai_response_sanitized = call_groq(sanitized_prompt)

    # UNCOMMENT CODE FOR QA TESTING
    # Requires the text1, text2, and textresponse .txt files in ./PrivPrompt/ (can reconfigure it as you like)
    # Also requires the pii_data.json file. Uncomment import json when using this file
    # Must run app.py inside the ./PrivPrompt/ folder (can reconfigure it as you like)
    #   python my-flask-app/app.py
    #
    # # Appends both responses to textresponse.txt with 5 newlines between (empty file once in a while)
    # with open("../PrivPrompt/textresponse.txt", "a", encoding="utf-8") as f:
    #     f.write(ai_response_original + "\n" * 5 + ai_response_sanitized + "\n" * 5)

    # # Writes each response to its own file (overwriting existing content)
    # with open("../PrivPrompt/text1.txt", "w", encoding="utf-8") as f1:
    #     f1.write(ai_response_original)

    # with open("../PrivPrompt/text2.txt", "w", encoding="utf-8") as f2:
    #     f2.write(ai_response_sanitized)

    # # Writes the dictionaries of collected PII into the pii_data.json file
    # with open("../PrivPrompt/pii_data.json", "w", encoding="utf-8") as f:
    #     json.dump({
    #         "emails": dict_email,
    #         "ssns":   dict_ssn,
    #         "names":  dict_name
    #     }, f, indent=2)


    return jsonify({
        "result": sanitized_prompt,
        "detected": {
            "emails": dict_email,
            "ssns": dict_ssn,
            "names": dict_name
        },
        "ai_original": ai_response_original,
        "ai_sanitized": ai_response_sanitized
    })

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch('templates/*')
    server.watch('static/*')
    server.serve(port=5001, debug=True)
