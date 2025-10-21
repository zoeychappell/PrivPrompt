import os
import sys
import subprocess
from pathlib import Path

def run_command(command):
    # Prints the command being ran. 
    print(f"\n\033[1;34mRunning: \033[1;36m{command}\033[0m")
    # Runs the command and grabs the result
    result = subprocess.run(command, shell=True)
    # If return code is anything but 0 (good)
    if result.returncode !=0:
        # Show why the command failed
        print(f"\033[0;31m❌  Command failed: {command}\033[0m")
        # Gracefully exit
        sys.exit(1)

'''
Checks the Python version for compatibility (3.8+)
'''
def check_python_version():
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✅ \033[1;34mPython version OK: {sys.version.split()[0]}\033[0m")

'''
Install the dependencies in requirements.txt
'''
def install_requirements():
    # Checks that the requirements.txt can be found
    if not Path("requirements.txt").exists():
        # If not, prints to the user
        print("❌\033[0;31m requirements.txt not found.\033[0m")
        # And exits gracefully
        sys.exit(1)
    # Runs command to install requirements
    run_command("pip install -r requirements.txt")
    print("✅ \033[1;34mDependencies installed.\033[0m")

'''
Install and donwload the required spaCy models
'''  
def setup_spacy_model():
    print("\n\033[1;34mSetting up spaCy...\033[0m")
    # Runs the setup command
    run_command("python -m spacy download en_core_web_lg")
    print("✅ \033[1;34mspaCy language model installed.\033[0m")

    
"Create the .env file. "
def create_env_file():
    env_path = Path(".env")
    if env_path.exists():
        print("✅ \033[1;34m .env file already exists — skipping creation.\033[0m")
        return

    print("\n\033[1;34m Creating .env file...\033[0m")
    api_keys = {
        "GROQ_API_KEY": "Groq",
        "COHERE_API_KEY": "Cohere",
        "GEMINI_API_KEY": "Google AI Studio (Gemini)",
        "DEEPSEEK_API_KEY": "Deepseek (via OpenRouter)"
    }

    with open(env_path, "w") as f:
        for key, name in api_keys.items():
            value = input(f"\033[1;34mEnter your {name} API key (or leave blank to skip): \033[0m").strip()
            if value:
                f.write(f"{key}='{value}'\n")

    print("✅\033[1;34m .env file created and keys saved.\033[0m")

'''
Create and activate the virtual environemnt. 
'''
def setup_virtualenv():
    venv_dir = Path("venv")
    if not venv_dir.exists():
            run_command(f"{sys.executable} -m venv venv")
            print("✅ \033[1;34mVirtual environment created.\033[0m")
            print("\n\033[1;34mTo activate it:")
            print("  - On macOS/Linux: source venv/bin/activate")
            print("  - On Windows: venv\\Scripts\\activate\033[0m")
    else:
        print("✅\033[1;34m Virtual environment already exists.\033[0m")

def main(): 
    print("+" * 50)
    print("\033[1;34mPrivPrompt Environmental Setup Utility\033[0m")
    print("+" * 50)
    check_python_version()
    setup_virtualenv()
    install_requirements()
    setup_spacy_model()
    create_env_file()

    print("\n🎉\033[1;32m Setup complete!")
    print("\033[1;34mNext steps:")
    print("1. Activate your virtual environment (if created).")
    print("2. Run your Flask app with: python app.py")
    print("3. Visit http://127.0.0.1:5001 in your browser.\033[0m")


if __name__ == "__main__":
    main()