'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint
py
CSEC-490, Rochester Institute of Technology
'''
import os
from groq import Groq
from dotenv import load_dotenv

'''Reaches out to groq and can get a response'''
def groq(user_input): 
    load_dotenv()

    API_KEY = os.getenv('api_token')
    client = Groq(api_key = API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": user_input,
            }
        ],
    model="llama-3.3-70b-versatile",
    )
    print(chat_completion.choices[0].message.content)


def main():
    groq("give me 5 random words")


if __name__ == '__main__':
    main()