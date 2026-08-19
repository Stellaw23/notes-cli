import os
import requests
from dotenv import load_dotenv

load_dotenv()

deepseek_key = os.environ.get("DEEPSEEK_API_KEY")

def call_deepseek(prompt):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {deepseek_key}",
    }
    body = {
        "model": "deepseek-v4-flash",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers,json=body)
    return response.json()