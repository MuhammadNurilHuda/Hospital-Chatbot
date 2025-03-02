# tests\test_database.py

import pytest
from app.database import Base, engine, SessionLocal, Appointment

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
    Menguji operasi insert data ke dalam tabel 'appointments'.
    
    Test ini melakukan langkah-langkah sebagai berikut:
    1. Membuat instance Appointment baru dengan data uji.
    2. Menambahkan instance tersebut ke session dan melakukan commit.
    3. Melakukan refresh pada instance untuk mendapatkan nilai-nilai terbaru (misalnya, ID yang dihasilkan).
    4. Memastikan bahwa:
       - Data telah tersimpan dengan benar (misalnya, data name, phone, dan doctor_specialist sesuai).
       - Appointment mendapatkan ID yang berarti telah berhasil disimpan di database.
    """
    db = SessionLocal()
    try:
        new_appointment = Appointment(
            name = "test",
            phone = "08123456789",
            doctor_specialist = "test",
            appointment_date = "2025-03-10"
        )
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        assert new_appointment.id is not None

        check_appointment = db.query(Appointment).filter_by(id=new_appointment.id).first()
        assert check_appointment is not None
        assert check_appointment.name == "test"
    
    finally:
        db.close()