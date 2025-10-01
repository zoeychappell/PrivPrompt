'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint

CSEC-490, Rochester Institute of Technology
'''
import os
from dotenv import load_dotenv
from openai import OpenAI
'''Currently not working because the tokens aren't free'''
def chatgpt_api():
    load_dotenv()

    API_KEY = os.getenv('chat_gpt_api_key')
    client = OpenAI(api_key=API_KEY)

    response = client.responses.create(
        model="gpt-5",
        input="Write a one-sentence bedtime story about a unicorn."
    )


def main():
    chatgpt_api()
if __name__ == '__main__':
    main()
