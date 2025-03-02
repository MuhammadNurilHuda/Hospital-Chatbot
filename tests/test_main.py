# tests\test_main.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

@pytest.fixture(scope='module', autouse=True)
def setup_database():
    """
    Fixture untuk menyiapkan database testing.
    
    Fungsi ini akan membuat semua tabel pada database sebelum seluruh test dijalankan,
    dan menghapus tabel-tabel tersebut setelah semua test selesai.
    Hal ini memastikan bahwa setiap test berjalan pada lingkungan database yang bersih.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_root_endpoint():
    """
    Menguji endpoint root ('/').
    
    Test ini mengirimkan GET request ke root endpoint dan memverifikasi:
    - Status code harus 200.
    - Response JSON harus mengandung pesan status yang sesuai.
    """
    response=client.get("/")
    assert response.status_code==200
    assert response.json() == {"message": "Hospital Chatbot API is running!"}

def test_chat():
    """
    Menguji endpoint '/chat' untuk kasus input dengan intent booking.
    
    Test ini mengirimkan POST request dengan pesan yang mengandung kata kunci 
    booking (misal, "booking", "reservasi"), kemudian memverifikasi bahwa respons
    menginstruksikan pengguna untuk mengisi informasi booking.
    """
    payload = {"message":"saya mau booking dokter"}
    response = client.post("/chat", json=payload)
    assert response.status_code==200
    data = response.json()
    assert "Silakan berikan informasi berikut:" in data["response"]

def test_appointment_booking_success():
    """
    Menguji endpoint '/appointment/book' dengan data appointment yang valid.
    
    Test ini mengirimkan POST request dengan payload data appointment yang lengkap
    dan memverifikasi:
    - Status code harus 200.
    - Response JSON mengandung pesan sukses dan key 'appointment_id' yang menunjukkan
      data telah berhasil disimpan di database.
    """
    appointment_data = {
        "name": "John Doe",
        "phone": "08123456789",
        "doctor_specialist": "Cardiology",
        "appointment_date": "2025-03-10"
    }
    response = client.post("/appointment/book", json=appointment_data)
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == "Appointment booked succesfully"
    assert "appointment_id" in data

def test_appointment_booking_invalid_date():
    """
    Menguji endpoint '/appointment/book' dengan format tanggal yang tidak valid.
    
    Test ini mengirimkan payload dengan tanggal yang salah format dan memverifikasi 
    bahwa FastAPI mengembalikan error validasi dengan status code 422.
    """
    appointment_data = {
        "name": "Jane Doe",
        "phone": "08129876543",
        "doctor_specialist": "Dermatology",
        "appointment_date": "invalid-date"
    }
    response = client.post("/appointment/book", json=appointment_data)
    assert response.status_code == 422

def test_appointment_booking_missing_field():
    """
    Menguji endpoint '/appointment/book' dengan field yang hilang.
    
    Test ini mengirimkan payload yang tidak menyertakan field 'doctor_specialist' dan 
    memverifikasi bahwa FastAPI mengembalikan error validasi (status code 422).
    """
    appointment_data = {
        "name": "Alice",
        "phone": "08123450000",
        "appointment_date": "2025-04-15"
    }
    response = client.post("/appointment/book", json=appointment_data)
    assert response.status_code == 422