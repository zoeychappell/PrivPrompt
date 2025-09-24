'''
PrivPrompt

Zoey Chappell, Adam Braccia, Minn Myint
py
CSEC-490, Rochester Institute of Technology
'''
from dotenv import load_dotenv
from google import genai
import os

'''
This function reaches out to the Google AI Studio AI API. 
Parameters:
    - sanitized_message : string 
Returns: 
    - response.text : string, LLM response to the prompt'''
def call_genai(sanitized_message):
    # Load the environment keys needed
    load_dotenv()
    # Fetch the API Key
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    # Create an API client and feed the API Key
    client = genai.Client(api_key=GEMINI_API_KEY)
    # Call the API and grab the response
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=sanitized_message
    )
    return response.text

