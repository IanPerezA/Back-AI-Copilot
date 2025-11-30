# tests/test_chat_api.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint():
    payload = {
        "user_input": "Hola, me llamo Ian",
        "session_id": "test123"
    }

    r = client.post("/api/chat", json=payload)
    print(">> RESPONSE JSON:", r.json())
    
    assert r.status_code == 200
    data = r.json()

    assert "response" in data
    assert data["intent"] == "default"
    assert data["session_id"] == "test123"
    assert "provider" in data
    assert "model" in data
