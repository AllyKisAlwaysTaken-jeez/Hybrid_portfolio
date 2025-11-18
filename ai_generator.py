import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_response(industry: str, style: str, goals: str):
    if not OPENAI_API_KEY:
        return "❌ Missing API key."
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a portfolio-building assistant."},
            {"role": "user", "content": f"Industry: {industry}\nStyle: {style}\nGoals: {goals}\nGenerate portfolio advice."}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    if "choices" not in data:
        return f"❌ Unexpected response: {data}"
    return data["choices"][0]["message"]["content"]
