"""Small wrapper around the Gemini API (google-genai SDK). Owner: Hijaz.

Get a free key: https://aistudio.google.com  ->  Get API key
Put it in .streamlit/secrets.toml (GEMINI_API_KEY = "...") or as an environment variable.
All functions return None on any error, so the app keeps working without Gemini.
"""
import json
import re
from utils import config

_client = None


def get_client():
    global _client
    if _client is None:
        key = config.get_gemini_key()
        if not key:
            return None
        from google import genai
        _client = genai.Client(api_key=key)
    return _client


def ask(prompt: str) -> str | None:
    """Send a prompt, return plain text (or None if Gemini is unavailable)."""
    client = get_client()
    if client is None:
        return None
    try:
        response = client.models.generate_content(model=config.GEMINI_MODEL, contents=prompt)
        return (response.text or "").strip()
    except Exception as e:  # rate limit, network, bad key...
        print(f"[gemini] error: {e}")
        return None


def ask_json(prompt: str):
    """Ask Gemini for JSON and parse it. Returns a Python object or None."""
    text = ask(prompt + "\n\nReturn ONLY valid JSON. No markdown, no explanation.")
    if not text:
        return None
    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"[gemini] could not parse JSON: {text[:200]}")
        return None
