'''
Zoey Chappell, Adam Braccia, Minn Myint
py
CSEC-490, Rochester Institute of Technology
'''

from openai import OpenAI
from dotenv import load_dotenv
import os
'''This function calls out to the Deepseek API through the OpenRouter
API. This means that the program doesn't actually communicate with deepseek
only with open router. '''
def call_deepseek(message):
    load_dotenv()

    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=DEEPSEEK_API_KEY,
    )
    completion = client.chat.completions.create(

    model="deepseek/deepseek-chat-v3.1:free",
    messages=[
        {
        "role": "user",
        "content": message
        }
    ]
    )
    print(completion.choices[0].message.content)

