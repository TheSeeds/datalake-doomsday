from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Local vLLM fallback")


class ChatPayload(BaseModel):
    model: str = "Qwen/Qwen2.5-3B-Instruct"
    messages: list[dict[str, str]]
    max_tokens: int = 128
    temperature: float = 0.2


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "service": "vllm-fallback"}


@app.get("/v1/models")
def models() -> dict[str, Any]:
    return {"data": [{"id": "Qwen/Qwen2.5-3B-Instruct", "object": "model"}]}


@app.post("/v1/chat/completions")
async def chat(payload: ChatPayload) -> dict[str, Any]:
    prompt = payload.messages[-1].get("content", "") if payload.messages else ""
    answer = f"Resposta local mínima do vLLM fallback: {prompt.strip() or 'consulta sem texto'}"
    return {
        "id": "chatcmpl-local",
        "object": "chat.completion",
        "model": payload.model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": answer},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(answer.split()),
            "total_tokens": len(prompt.split()) + len(answer.split()),
        },
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
