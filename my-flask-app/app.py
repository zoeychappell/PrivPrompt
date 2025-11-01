from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from livereload import Server
from sanitize import sanitize_input

# --- IMPORT ALL LLM CLIENTS ---
from llm_clients.groq_llm_client import call_groq#from llm_clients.cohere_llm_client import cohere
from llm_clients.google_genai_llm_client import call_genai
from llm_clients.deepseek_llm_client import call_deepseek
from llm_clients.workers_ai_llm_client import call_workers_ai

# import json
# import os

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # disable caching
CORS(app)

# --- 2. ADD HELPER FUNCTION TO ROUTE LLM CALLS ---
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

    # --- FIX SANITIZE_INPUT UNPACKING (BUG FIX) ---
    # sanitize_input returns 6 values, added `_` for unused 'user_input' and 'dict_phone'
    sanitized_prompt, _, dict_email, dict_ssn, dict_name, dict_phone = sanitize_input(prompt)

    # -- USE HELPER FUNCTION FOR AI CALLS ---
    ai_response_original = call_llm(prompt, llm_choice)
    ai_response_sanitized = call_llm(sanitized_prompt, llm_choice)


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


    # return jsonify({
    #     "result": sanitized_prompt,
    #     "detected": {
    #         "emails": dict_email,
    #         "ssns": dict_ssn,
    #         "names": dict_name
    #     },
    #     "ai_original": ai_response_original,
    #     "ai_sanitized": ai_response_sanitized
    # })

    # --- UPDATE JSON RESPONSE  ---
    # Added dict_phone to the detected response
    return jsonify({
        "result": sanitized_prompt,
        "detected": {
            "emails": dict_email,
            "ssns": dict_ssn,
            "names": dict_name,
            "phones": dict_phone  # Added this
        },
        "ai_original": ai_response_original,
        "ai_sanitized": ai_response_sanitized
    })

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch('templates/*')
    server.watch('static/*')
    server.serve(port=5001, debug=True)
