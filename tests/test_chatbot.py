# tests\test_chatbot.py
"""
Unit test untuk fungsi `get_response` di app/chatbot.py:
- Booking intent: langsung mengembalikan instruksi.
- Non-booking intent: memanggil RAG chain (di-stub) dan mengembalikan jawaban chain.
"""

import pytest
from app.chatbot import get_response, BOOKING_KEYWORDS
from langchain.chains import ConversationalRetrievalChain

def test_get_response_booking_intent():
    """
    Pastikan jika input mengandung kata kunci booking,
    fungsi langsung kembalikan instruksi, tanpa memanggil RAG chain.
    """
    sample = "Saya mau Reservasi dokter gigi"
    res = get_response(sample, session_id="sess1")
    assert "Silakan berikan informasi berikut" in res

def test_get_response_rag_chain(monkeypatch):
    """
    Untuk input non-booking, stub RAG chain agar mengembalikan jawaban spesifik,
    lalu pastikan get_response men‐return jawaban itu.
    """
    # Buat DummyChain yang selalu return answer tertentu
    class DummyChain:
        def __call__(self, inputs):
            return {"answer": "Dummy RAG reply"}

    # Stub from_llm pada class ConversationalRetrievalChain
    monkeypatch.setattr(
        ConversationalRetrievalChain,
        "from_llm",
        lambda *args, **kwargs: DummyChain()
    )

    # Panggil dengan pesan yang tidak ada keyword booking
    res = get_response("Tolong informasikan jadwal UGD", session_id="sess2")
    assert res == "Dummy RAG reply"
