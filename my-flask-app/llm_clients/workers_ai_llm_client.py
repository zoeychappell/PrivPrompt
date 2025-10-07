'''
Zoey Chappell, Adam Braccia, Minn Myint
py
CSEC-490, Rochester Institute of Technology
'''

from dotenv import load_dotenv
import os
import requests

def call_workers_ai(message):
    load_dotenv()
    WORKERS_API_KEY = os.getenv('WORKERS_API_KEY')
    WORKERS_ACCOUNT_ID = os.getenv('WORKERS_ACCOUNT_ID')

    inputs = [
        {"role":"system", "content":"You are a friendly assistant that helps answer questions."},
        {"role": "user", "content": message}
    ]

    API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{WORKERS_ACCOUNT_ID}/ai/run/"
    headers = {"Authorization": f"Bearer {WORKERS_API_KEY}"}

    API_URL = f"{API_BASE_URL}@cf/meta/llama-3-8b-instruct"
    payload = {"messages": inputs}  
    response = requests.post(API_URL, headers=headers, json=payload)

    # optional: check for errors
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")
    text = response.json()
    return text['result']['response']


