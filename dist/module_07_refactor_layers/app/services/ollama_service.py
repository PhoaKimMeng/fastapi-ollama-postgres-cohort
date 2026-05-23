import httpx
from fastapi import HTTPException

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"
def call_ollama(question: str, system_prompt: str) -> str:
    try:
        with httpx.Client(timeout=60.0) as client:
            r = client.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                "stream": False,
            })
            r.raise_for_status()
            return r.json()["message"]["content"]
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Ollama is not reachable.")
