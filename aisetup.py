from openai import OpenAI

def authenticate(api_key):
    global client
    client = OpenAI(api_key=api_key)

def get_llm_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content