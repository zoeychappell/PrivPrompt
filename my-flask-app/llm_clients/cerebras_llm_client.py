import os
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

def call_cerebras(prompt):
    load_dotenv()
    response_text = ""

    client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))
    # Create the stream
    stream = client.chat.completions.create(
        # Send the message
        messages=[
            {
                "role": "system",
                # Fill in the prompt
                "content": prompt
            }
        ],
        # Model settings
        model="llama-3.3-70b",
        stream=True,
        max_completion_tokens=2048,
        temperature=0.2,
        top_p=1
        )
    # iterate through each chunk and concat them together
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            # Accumulate the chunks together
            response_text += delta            

    return response_text.strip() 

