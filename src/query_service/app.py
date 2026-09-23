import os
from typing import Any

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="TheSeed Query Service", version="0.1.0")

MODEL_ENDPOINT = os.getenv(
    "MODEL_ENDPOINT",
    "http://192.168.56.12:8000/v1/chat/completions",
)
FALLBACK_ENDPOINT = os.getenv(
    "FALLBACK_ENDPOINT",
    "http://192.168.56.12:8001/v1/chat/completions",
)
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-0.5B-Instruct")


class QueryRequest(BaseModel):
    prompt: str
    max_tokens: int = 128
    temperature: float = 0.2


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "query-service",
        "model": MODEL_NAME,
        "model_endpoint": MODEL_ENDPOINT,
        "fallback_endpoint": FALLBACK_ENDPOINT,
    }


async def _call_completion(
    endpoint: str, payload: QueryRequest
) -> dict[str, Any]:
    request_body = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": payload.prompt}],
        "max_tokens": payload.max_tokens,
        "temperature": payload.temperature,
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(endpoint, json=request_body)
        response.raise_for_status()
        return response.json()


@app.post("/query")
async def query(payload: QueryRequest) -> dict[str, Any]:
    first_error: Exception | None = None

    try:
        data = await _call_completion(MODEL_ENDPOINT, payload)
    except Exception as exc:  # noqa: BLE001
        first_error = exc
        data = None

    if data is None:
        try:
            data = await _call_completion(FALLBACK_ENDPOINT, payload)
        except Exception as exc:  # noqa: BLE001
            first_error = exc
            data = None

    if data is None:
        return {
            "answer": "",
            "raw": None,
            "error": str(first_error),
            "fallback_used": True,
        }

    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return {
        "answer": content,
        "raw": data,
        "fallback_used": first_error is not None,
    }
