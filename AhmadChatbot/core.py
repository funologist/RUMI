"""
core.py - Shared Rumi chatbot logic (Groq API wrapper).
Used by both main.py (CLI) and app.py (web).
"""

import os
import sys
from groq import Groq
from dotenv import load_dotenv

MODEL = "openai/gpt-oss-20b"
SYSTEM_PROMPT = (
    "You are Rumi, a helpful and friendly AI chat assistant. "
    "Keep answers clear and concise unless the user asks for more detail."
)
MAX_HISTORY_MESSAGES = 20  # trims history so context doesn't grow forever


def load_client() -> Groq:
    """Load the Groq client using the API key from .env."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not found. Copy .env.example to .env and add your key.")
        sys.exit(1)
    return Groq(api_key=api_key)


def new_conversation() -> list:
    """Return a fresh message list seeded with the system prompt."""
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def trim_history(messages: list) -> list:
    """Keep the system prompt + the most recent N messages."""
    system = messages[0]
    rest = messages[1:]
    if len(rest) > MAX_HISTORY_MESSAGES:
        rest = rest[-MAX_HISTORY_MESSAGES:]
    return [system] + rest


def get_response(client: Groq, messages: list) -> str:
    """Send the conversation to Groq and return the assistant's reply."""
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[Error talking to Groq API: {e}]"
