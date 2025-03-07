# tests\test_database.py

import pytest
from app.database import Base, engine, SessionLocal, Appointment, UserActivityLog

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """
    Fixture untuk menyiapkan lingkungan database untuk testing.
    
    Fungsi ini melakukan:
    - Pembuatan semua tabel yang didefinisikan dalam metadata (misalnya, tabel 'appointments')
      sebelum seluruh test dijalankan.
    - Penghapusan tabel-tabel tersebut setelah seluruh test selesai.
    
    Dengan cara ini, setiap test berjalan pada lingkungan database yang bersih sehingga
    tidak terjadi interferensi antara data dari test satu dengan test lainnya.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_database_connection():
    """
    Menguji koneksi ke database dengan membuat session dan menjalankan query sederhana.
    
    Test ini memastikan:
    - Koneksi ke database dapat dibuat dengan benar.
    - Tabel 'appointments' sudah tersedia, sehingga query count menghasilkan 0
      (karena belum ada data yang dimasukkan).
    """
    db = SessionLocal()
    try:
        count = db.query(Appointment).count()
        assert count == 0
    finally:
        db.close()

def test_insert_appointment():
    """
    Menguji penyimpanan data ke tabel 'appointments'.
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
        
        assert new_appointment.id is not None
        saved_appointment = db.query(Appointment).filter_by(id=new_appointment.id).first()
        assert saved_appointment is not None
        assert saved_appointment.name == "Test User"
        assert saved_appointment.doctor_specialist == "Test Specialist"
    finally:
        db.close()

def test_insert_user_activity():
    """
    Menguji penyimpanan data ke tabel 'user_activity_logs'.
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
        
        # Pastikan ID-nya terisi, menandakan data berhasil masuk
        assert new_log.id is not None
        
        # Verifikasi data di database
        stored_log = db.query(UserActivityLog).filter_by(id=new_log.id).first()
        assert stored_log is not None
        assert stored_log.prompt == "Halo Dokter, saya sakit apa?"
        assert stored_log.response == "Mohon ceritakan gejalanya lebih lengkap."
    finally:
        db.close()