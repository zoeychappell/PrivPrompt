from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from livereload import Server
from sanitize import sanitize_input
from llm_clients.groq_llm_client import call_groq
# import json
# import os

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


    # # UNCOMMENT CODE FOR QA TESTING
    # # The code will automatically add text1, text2, and textresponse .txt files in ./QAFolder/ if missing
    # # Also adds the pii_data.json file. Uncomment import json and import os when using this part
    # # Must run app.py inside the ./my-flask-app/ folder
    # #   python app.py

    # # --- Ensure files exist ---
    # required_files = {
    #     "text1.txt": "",
    #     "text2.txt": "",
    #     "textresponse.txt": "",
    #     "pii_data.json": {
    #         "emails": {},
    #         "ssns": {},
    #         "names": {},
    #         "prompt": "",
    #         "sanitized_prompt": ""
    #     }
    # }

    # for filename, default_content in required_files.items():
    #     path = os.path.join("./QAFolder/", filename)
    #     if not os.path.exists(path):
    #         if filename.endswith(".json"):
    #             with open(path, "w", encoding="utf-8") as f:
    #                 json.dump(default_content, f, indent=2)
    #         else:
    #             with open(path, "w", encoding="utf-8") as f:
    #                 f.write("")

    # # Appends both responses to textresponse.txt with 5 newlines between (empty file once in a while)
    # with open("./QAFolder/textresponse.txt", "a", encoding="utf-8") as f:
    #     f.write(ai_response_original + "\n" * 5 + ai_response_sanitized + "\n" * 5)

    # # Writes each response to its own file (overwriting existing content)
    # with open("./QAFolder/text1.txt", "w", encoding="utf-8") as f1:
    #     f1.write(ai_response_original)

    # with open("./QAFolder/text2.txt", "w", encoding="utf-8") as f2:
    #     f2.write(ai_response_sanitized)

    # # Writes the dictionaries of collected PII into the pii_data.json file
    # with open("./QAFolder/pii_data.json", "w", encoding="utf-8") as f:
    #     json.dump({
    #         "emails": dict_email,
    #         "ssns":   dict_ssn,
    #         "names":  dict_name,
    #         "prompt": prompt,
    #         "sanitized_prompt": sanitized_prompt
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
