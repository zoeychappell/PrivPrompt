from mistralai import Mistral
from dotenv import load_dotenv
import os


def call_mistral(prompt):
    load_dotenv()

    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

    with Mistral(
        api_key=MISTRAL_API_KEY,
    ) as mistral:

        res = mistral.chat.complete(model="mistral-small-latest", messages=[
            {
                "content": prompt,
                "role": "user",
            },
        ], stream=False)

        # Handle response
    return res.choices[0].message.content

def main():
    response = call_mistral("Tell me who the best painter is")
    print(response)
if __name__ == '__main__':
    main()

