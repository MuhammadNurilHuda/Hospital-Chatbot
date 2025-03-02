# tests\test_chatbot.py

import pytest
from app.chatbot import get_response, BOOKING_KEYWORDS

def test_get_response():
    """
    Menguji fungsi get_response ketika input mengandung kata kunci booking.
    Fungsi seharusnya mengembalikan instruksi untuk mengisi informasi booking.
    """
    test_message = "Saya ingin reservasi dokter"
    response = get_response(test_message)
    assert "Silakan berikan informasi" in response

def test_get_general_response(monkeypatch):
    """
    Menguji fungsi get_response untuk input non-booking.
    Fungsi DeepSeek API asli digantikan dengan dummy_create monkeypatch yang mengembalikan response terkontrol.
    """
    test_message = "Apa kabar?"

    # Objek dummy untuk response dari deepseek API
    class DummyMessage():
        content = "Ini response dari DeepSeek API..."

    class DummyChoice():
        message = DummyMessage()

    class DummyResponse():
        choices = [DummyChoice()]
    
    def dummy_create(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr("app.chatbot.client.chat.completions.create", dummy_create)

    response = get_response(test_message)
    assert response == "Ini response dari DeepSeek API..."