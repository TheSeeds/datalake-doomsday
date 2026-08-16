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


class QueryRequest(BaseModel):
    prompt: str
    max_tokens: int = 128
    temperature: float = 0.2


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "query-service",
        "model_endpoint": MODEL_ENDPOINT,
    }


@app.post("/query")
async def query(payload: QueryRequest) -> dict[str, Any]:
    request_body = {
        "model": "Qwen/Qwen2.5-3B-Instruct",
        "messages": [{"role": "user", "content": payload.prompt}],
        "max_tokens": payload.max_tokens,
        "temperature": payload.temperature,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(MODEL_ENDPOINT, json=request_body)
        response.raise_for_status()
        data = response.json()

    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return {
        "answer": content,
        "raw": data,
    }
