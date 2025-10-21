import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    # Prints the command being ran. 
    print(f"\n Running: {command}")
    # Runs the command and grabs the result
    result = subprocess.run(command, shell=True)
    # If return code is anything but 0 (good)
    if result.returncode !=0:
        # Show why the command failed
        print(f"⚠️  Command failed: {command}")
        # Gracefully exit
        sys.exit(1)

'''
Checks the Python version for compatibility (3.8+)
'''
def check_python_version():
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✅ Python version OK: {sys.version.split()[0]}")

'''
Install the dependencies in requirements.txt
'''
def install_requirements():
    # Checks that the requirements.txt can be found
    if not Path("requirements.txt").exists():
        # If not, prints to the user
        print("❌ requirements.txt not found.")
        # And exits gracefully
        sys.exit(1)
    # Runs command to install requirements
    run_command("pip install -r requirements.txt")
    print("✅ Dependencies installed.")

'''
Install and donwload the required spaCy models
'''  
def setup_spacy_model():
    print("\nSetting up spaCy...")
    # Runs the setup command
    run_command("python -m spacy download en_core_web_lg")
    print("✅ spaCy language model installed.")
"Create the .env file. "
def create_env_file():
    env_path = Path(".env")
    if env_path.exists():
        print("✅ .env file already exists — skipping creation.")
        return

    print("\nCreating .env file...")
    api_keys = {
        "GROQ_API_KEY": "Groq",
        "COHERE_API_KEY": "Cohere",
        "GEMINI_API_KEY": "Google AI Studio (Gemini)",
        "DEEPSEEK_API_KEY": "Deepseek (via OpenRouter)"
    }

    with open(env_path, "w") as f:
        for key, name in api_keys.items():
            value = input(f"Enter your {name} API key (or leave blank to skip): ").strip()
            if value:
                f.write(f"{key}='{value}'\n")

    print("✅ .env file created and keys saved.")

'''
Create and activate the virtual environemnt. 
'''
def setup_virtualenv():
    venv_dir = Path("venv")
    if not venv_dir.exists():
            run_command(f"{sys.executable} -m venv venv")
            print("✅ Virtual environment created.")
            print("\nTo activate it:")
            print("  - On macOS/Linux: source venv/bin/activate")
            print("  - On Windows: venv\\Scripts\\activate")
    else:
        print("✅ Virtual environment already exists.")

def main(): 
    print("+" * 50)
    print("PrivPrompt Environmental Setup Utility")
    print("+" * 50)

    check_python_version()
    setup_virtualenv()
    install_requirements()
    setup_spacy_model()
    create_env_file()

    print("\n🎉 Setup complete!")
    print("Next steps:")
    print("1. Activate your virtual environment (if created).")
    print("2. Run your Flask app with: python app.py")
    print("3. Visit http://127.0.0.1:5001 in your browser.")


if __name__ == "__main__":
    main()