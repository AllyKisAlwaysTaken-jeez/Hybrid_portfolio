import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_text(prompt: str, max_length: int = 180) -> str:
    """
    Generates rewritten portfolio text using OpenAI API instead of local GPT-2.
    Fully compatible with free Render deployment.
    """
    if not OPENAI_API_KEY:
        return "❌ Missing API key. Please set your OPENAI_API_KEY environment variable."

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",  # You can also use "gpt-4" if you prefer
        "messages": [
            {"role": "system", "content": "You are a portfolio content rewriting assistant."},
            {"role": "user", "content": f"{prompt}"}
        ],
        "temperature": 0.7,
        "max_tokens": max_length
    }

    response = requests.post(url, headers=headers, json=payload)
    
    try:
        data = response.json()
    except Exception as e:
        return f"❌ Failed to parse API response: {str(e)}"

    if "error" in data:
        ret
