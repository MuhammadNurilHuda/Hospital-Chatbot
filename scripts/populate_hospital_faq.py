#!/usr/bin/env python3
# scripts/populate_hospital_faq.py

from app.database import SessionLocal, engine, Base
from app.models import HospitalFAQ

def main():
    # Pastikan tabel sudah ada
    Base.metadata.create_all(bind=engine)

    dummy = [
        {
            "question": "Bagaimana cara membuat janji temu?",
            "answer": "Anda dapat membuat janji temu melalui endpoint /appointment/book dengan mengisi nama, nomor telepon, spesialisasi dokter, dan tanggal janji."
        },
        {
            "question": "Apa saja jam operasional rumah sakit?",
            "answer": "Rumah sakit buka setiap hari Senin–Sabtu pukul 08:00–20:00."
        },
        {
            "question": "Dokumen apa yang perlu dibawa saat tiba?",
            "answer": "Silakan bawa KTP, kartu asuransi (jika ada), dan hasil laboratorium sebelumnya (jika relevan)."
        },
        {
            "question": "Bagaimana prosedur pembatalan janji temu?",
            "answer": "Anda dapat membatalkan janji temu dengan menghubungi call center kami minimal 24 jam sebelum jadwal."
        },
        {
            "question": "Apakah metode pembayaran yang diterima?",
            "answer": "Kami menerima pembayaran tunai, kartu debit/kredit, dan asuransi rekanan."
        },
    ]

    db = SessionLocal()
    try:
        for item in dummy:
            faq = HospitalFAQ(
                question=item["question"],
                answer=item["answer"]
            )
            db.add(faq)
        db.commit()
        print(f"✅ Memasukkan {len(dummy)} baris ke hospital_faq")
    except Exception as e:
        db.rollback()
        print("❌ Error saat memasukkan data hospital_faq:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()