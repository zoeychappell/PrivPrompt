'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint
py
CSEC-490, Rochester Institute of Technology
'''
import os
from cohere import ClientV2
from dotenv import load_dotenv

def cohere(user_input):
    load_dotenv()

    CO_API_KEY = os.getenv('COHERE_API_KEY')
    co = ClientV2(CO_API_KEY)
    response = co.chat(
        model="command-a-03-2025", 
        messages=[{"role": "user", "content": user_input}]
        )
    llm_output = response.message.content[0].text
    return llm_output

def main():
    cohere("test")

if __name__ == '__main__':
    main()