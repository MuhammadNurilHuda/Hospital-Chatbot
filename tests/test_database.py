# tests/test_database.py
"""
Unit tests untuk operasi database:
- Koneksi ke database
- Insert data ke tabel appointments dan user_activity_logs
"""

import pytest
from app.database import Base, engine, SessionLocal
from app.models import Appointment, UserActivityLog

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """
    Fixture untuk menyiapkan lingkungan database testing:
    - Membuat semua tabel sebelum test
    - Menghapus tabel setelah test selesai
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_database_connection():
    """
    Menguji bahwa koneksi ke database berhasil,
    dan tabel appointments sudah ada.
    """
    db = SessionLocal()
    try:
        count = db.query(Appointment).count()
        assert count == 0
    finally:
        db.close()

def test_insert_appointment():
    """
    Menguji penyimpanan data ke tabel appointments.
    """
    db = SessionLocal()
    try:
        new_appointment = Appointment(
            name="Test User",
            phone="0811111111",
            doctor_specialist="Test Specialist",
            appointment_date="2025-05-20"
        )
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        
        # Cek bahwa ID ter-generate
        assert new_appointment.id is not None

        # Verifikasi data di database
        saved = db.query(Appointment).filter_by(id=new_appointment.id).first()
        assert saved is not None
        assert saved.name == "Test User"
        assert saved.doctor_specialist == "Test Specialist"
    finally:
        db.close()

def test_insert_user_activity():
    """
    Menguji penyimpanan data ke tabel user_activity_logs.
    """
    db = SessionLocal()
    try:
        new_log = UserActivityLog(
            prompt="Halo Dokter, saya sakit apa?",
            response="Mohon ceritakan gejalanya lebih lengkap."
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)

        # Pastikan ID terisi
        assert new_log.id is not None

        # Cek isi kolom di database
        stored = db.query(UserActivityLog).filter_by(id=new_log.id).first()
        assert stored is not None
        assert stored.prompt == "Halo Dokter, saya sakit apa?"
        assert stored.response == "Mohon ceritakan gejalanya lebih lengkap."
    finally:
        db.close()
