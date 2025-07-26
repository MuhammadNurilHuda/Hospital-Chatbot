# tests/test_chat_endpoint.py

import os
import pytest
from fastapi.testclient import TestClient

# Override env sebelum import app
os.environ.setdefault("REDIS_URL", "redis://dummy:6379")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("DEEPSEEK_API_KEY", "testkey")

from app.main import app
import app.session as session_mod
import app.chatbot as chatbot_mod
from langchain.chains import ConversationalRetrievalChain

client = TestClient(app)

@pytest.fixture(autouse=True)
def stub_session_and_redis(monkeypatch):
    # Stub session functions
    monkeypatch.setattr(session_mod, "get_session", lambda sid: True)
    monkeypatch.setattr(session_mod, "create_session", lambda data: "test-session")
    monkeypatch.setattr(session_mod, "update_session", lambda sid, data: None)

    # Stub RedisChatMessageHistory agar tidak connect Redis
    class DummyHistory:
        def __init__(self, session_id, url):
            pass
        def add_user_message(self, msg): pass
        def add_ai_message(self, msg): pass
        def get_messages(self):
            return []

    monkeypatch.setattr(chatbot_mod, "RedisChatMessageHistory", DummyHistory)

def test_chat_booking_intent_returns_session_and_instruction():
    resp = client.post("/chat", json={"message": "Saya mau booking dokter jantung besok"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "test-session"
    assert "Silakan berikan informasi berikut" in data["response"]

def test_chat_rag_intent_uses_rag_chain(monkeypatch):
    class DummyChain:
        def __call__(self, inputs):
            return {"answer": "Jawaban RAG dummy"}

    # Stub chain factory
    monkeypatch.setattr(
        ConversationalRetrievalChain,
        "from_llm",
        lambda *args, **kwargs: DummyChain()
    )

    resp = client.post(
        "/chat",
        json={"message": "Apa jadwal dokter paru besok?"},
        headers={"session_id": "abc-session"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "abc-session"
    assert data["response"] == "Jawaban RAG dummy"
