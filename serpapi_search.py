import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def search_online(query: str):
    if not SERPAPI_KEY:
        raise RuntimeError("SERPAPI_KEY not set")

    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "gl": "in"
    }

    response = requests.get(
        "https://serpapi.com/search",
        params=params,
        timeout=30
    )
    response.raise_for_status()
    return response.json().get("local_results", [])
