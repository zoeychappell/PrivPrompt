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
def call_groq(user_input): 
    load_dotenv()

    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    client = Groq(api_key = GROQ_API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": user_input,
            }
        ],
    model="llama-3.3-70b-versatile",
    )
    llm_output = chat_completion.choices[0].message.content
    print(llm_output)
    return llm_output

def main():
    response = call_groq("give me 5 random words")

if __name__ == '__main__':
    main()