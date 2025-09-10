'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint
py
CSEC-490, Rochester Institute of Technology
'''
from openai import OpenAI
'''Currently not working because the tokens aren't free'''
def chatgpt_api():
    client = OpenAI(api_key="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")

    response = client.responses.create(
        model="gpt-5",
        input="Write a one-sentence bedtime story about a unicorn."
    )

    print(response.output_text)  

def main():
    chatgpt_api()
if __name__ == '__main__':
    main()
