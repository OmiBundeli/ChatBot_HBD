import os
import json
import requests
from dotenv import load_dotenv
from models import MODEL
from prompts import SQL_SYSTEM_PROMPT

load_dotenv()

API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def route_user_input(user_text: str) -> dict:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SQL_SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0,
        "max_tokens": 450
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    content = data["choices"][0]["message"]["content"].strip()
    return json.loads(content)
