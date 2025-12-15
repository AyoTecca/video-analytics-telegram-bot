import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
PROMPT_PATH = "llm_prompt.txt"

if not os.path.exists(PROMPT_PATH):
    raise RuntimeError("llm_prompt.txt not found")


def build_query(question: str) -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        "stream": False,
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()
    data = response.json()

    return data["message"]["content"].strip()
