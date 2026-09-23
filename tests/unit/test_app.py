import httpx
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "query-service"
    assert "Qwen" in body["model"]


def _ok_answer(content: str):
    return {
        "choices": [{"message": {"role": "assistant", "content": content}}],
        "usage": {"total_tokens": 1},
    }


def test_query_success(monkeypatch):
    import app as app_module

    async def fake_completion(endpoint, payload):
        return _ok_answer("resposta do modelo")

    monkeypatch.setattr(app_module, "_call_completion", fake_completion)
    response = client.post("/query", json={"prompt": "teste"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "resposta do modelo"
    assert body["fallback_used"] is False


def test_query_fallback_used(monkeypatch):
    import app as app_module

    state = {"calls": 0}

    async def fake_completion(endpoint, payload):
        state["calls"] += 1
        if state["calls"] == 1:
            raise httpx.ConnectError("primary down", request=None)
        return _ok_answer("resposta do fallback")

    monkeypatch.setattr(app_module, "_call_completion", fake_completion)
    response = client.post("/query", json={"prompt": "teste"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "resposta do fallback"
    assert body["fallback_used"] is True
    assert state["calls"] == 2


def test_query_all_endpoints_down(monkeypatch):
    import app as app_module

    async def fake_completion(endpoint, payload):
        raise httpx.ConnectError("all down", request=None)

    monkeypatch.setattr(app_module, "_call_completion", fake_completion)
    response = client.post("/query", json={"prompt": "teste"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == ""
    assert body["raw"] is None
    assert body["error"] is not None
    assert body["fallback_used"] is True


def test_query_missing_prompt_validation():
    response = client.post("/query", json={})
    assert response.status_code == 422