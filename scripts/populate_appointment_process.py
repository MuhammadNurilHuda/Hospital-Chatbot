#!/usr/bin/env python3
# scripts/populate_appointment_process.py

from app.database import SessionLocal, engine, Base
from app.models   import AppointmentProcess

def main():
    # Pastikan tabel sudah dibuat
    Base.metadata.create_all(bind=engine)

    dummy = [
        {
            "step_order": 1,
            "title": "Registrasi Pasien",
            "description": "Pasien mengisi formulir pendaftaran dengan data diri lengkap."
        },
        {
            "step_order": 2,
            "title": "Verifikasi Dokumen",
            "description": "Staf rumah sakit memeriksa kelengkapan dokumen dan asuransi."
        },
        {
            "step_order": 3,
            "title": "Penjadwalan",
            "description": "Pasien memilih tanggal dan waktu kunjungan ke dokter spesialis."
        },
        {
            "step_order": 4,
            "title": "Konfirmasi Booking",
            "description": "Sistem mengirimkan notifikasi konfirmasi lewat SMS/Email."
        },
        {
            "step_order": 5,
            "title": "Kedatangan Pasien",
            "description": "Pasien datang ke rumah sakit dan melakukan check‑in di loket."
        },
        {
            "step_order": 6,
            "title": "Pemeriksaan Dokter",
            "description": "Dokter melakukan konsultasi dan pemeriksaan medis."
        },
        {
            "step_order": 7,
            "title": "Pembayaran & Resepsi",
            "description": "Pasien melakukan pembayaran dan mendapatkan resep/rujukan."
        },
    ]

    db = SessionLocal()
    try:
        for item in dummy:
            step = AppointmentProcess(
                step_order=item["step_order"],
                title=item["title"],
                description=item["description"]
            )
            db.add(step)
        db.commit()
        print(f"✅ Memasukkan {len(dummy)} baris ke appointment_process")
    except Exception as e:
        db.rollback()
        print("❌ Error saat memasukkan data appointment_process:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()
