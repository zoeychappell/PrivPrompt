'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint
py
CSEC-490, Rochester Institute of Technology
'''
from dotenv import load_dotenv
from google import genai
import os


def call_genai():
    load_dotenv()

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents="Explain how AI works in a few words"
    )
    print(response.text)

def main():
    call_genai()

if __name__ == '__main__':
    main()
