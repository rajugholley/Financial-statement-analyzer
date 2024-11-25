# aisetup.py
from openai import OpenAI

# Make client global
client = None

def authenticate(api_key):
    """Initialize global OpenAI client"""
    global client
    client = OpenAI(api_key=api_key)

def get_llm_response(prompt):
    """Get response from OpenAI"""
    global client
    if client is None:
        raise Exception("Please authenticate first")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content