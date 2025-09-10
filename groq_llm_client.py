'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint
py
CSEC-490, Rochester Institute of Technology
'''
API_KEY = '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'
from groq import Groq
'''Reaches out to groq and can get a response'''
def groq(): 
    client = Groq(api_key = API_KEY)
    chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": "Explain the importance of fast language models",
            }
        ],
    model="llama-3.3-70b-versatile",
    )
    print(chat_completion.choices[0].message.content)


def main():
    groq()


if __name__ == '__main__':
    main()