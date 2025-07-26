#!/usr/bin/env python3
# scripts/populate_hospital_locations.py

from app.database import SessionLocal, engine, Base
from app.models   import HospitalLocation

def main():
    # Pastikan tabel ada
    Base.metadata.create_all(bind=engine)

    dummy = [
        {
            "name": "RS Harapan Sehat",
            "address": "Jl. Melati No. 10, Jakarta",
            "phone": "(021) 1234-5678"
        },
        {
            "name": "RS Bunga Teratai",
            "address": "Jl. Mawar No. 5, Bandung",
            "phone": "(022) 8765-4321"
        },
        {
            "name": "RS Pelita Hati",
            "address": "Jl. Kenanga No. 20, Surabaya",
            "phone": "(031) 2468-1357"
        },
        {
            "name": "RS Cahaya Medika",
            "address": "Jl. Flamboyan No. 3, Yogyakarta",
            "phone": "(0274) 555-123"
        },
        {
            "name": "RS Sejahtera",
            "address": "Jl. Anggrek No. 15, Medan",
            "phone": "(061) 9988-7766"
        },
    ]

    db = SessionLocal()
    try:
        for item in dummy:
            loc = HospitalLocation(
                name=item["name"],
                address=item["address"],
                phone=item["phone"]
            )
            db.add(loc)
        db.commit()
        print(f"✅ Memasukkan {len(dummy)} baris ke hospital_locations")
    except Exception as e:
        db.rollback()
        print("❌ Error saat memasukkan data hospital_locations:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()