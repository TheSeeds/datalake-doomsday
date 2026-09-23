from fastapi.testclient import TestClient

from fallback_vllm import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "vllm-fallback"


def test_models():
    response = client.get("/v1/models")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["object"] == "model"
    assert "Qwen" in data[0]["id"]


def test_chat_completion():
    payload = {
        "model": "Qwen/Qwen2.5-0.5B-Instruct",
        "messages": [{"role": "user", "content": "Hola"}],
    }
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["object"] == "chat.completion"
    assert body["model"] == "Qwen/Qwen2.5-0.5B-Instruct"
    assert body["choices"][0]["message"]["role"] == "assistant"
    assert "Resposta" in body["choices"][0]["message"]["content"]
    assert body["usage"]["prompt_tokens"] == 1


def test_chat_completion_empty_messages():
    payload = {"messages": []}
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    content = response.json()["choices"][0]["message"]["content"]
    assert "consulta sem texto" in content


def test_chat_completion_missing_model_uses_default():
    payload = {"messages": [{"role": "user", "content": "test"}]}
    response = client.post("/v1/chat/completions", json=payload)
    assert response.status_code == 200
    assert "0.5B" in response.json()["model"]