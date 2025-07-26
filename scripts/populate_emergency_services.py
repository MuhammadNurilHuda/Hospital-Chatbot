#!/usr/bin/env python3
# scripts/populate_emergency_services.py

from app.database import SessionLocal, engine, Base
from app.models   import EmergencyService

def main():
    Base.metadata.create_all(bind=engine)

    dummy = [
        {
            "service_name": "UGD 24 Jam",
            "description": "Unit Gawat Darurat buka 24 jam untuk kasus kritis.",
            "contact": "021-7889001 ext. 100"
        },
        {
            "service_name": "Ambulans",
            "description": "Layanan ambulans siap antar pasien ke rumah sakit.",
            "contact": "021-7889001 ext. 200"
        },
        {
            "service_name": "ICU",
            "description": "Intensive Care Unit dengan alat monitoring lengkap.",
            "contact": "021-7889001 ext. 300"
        },
        {
            "service_name": "Laboratorium Darurat",
            "description": "Tes laboratorium hasil cepat dalam 1 jam.",
            "contact": "021-7889001 ext. 400"
        },
        {
            "service_name": "Farmasi 24 Jam",
            "description": "Apotik rumah sakit buka 24 jam untuk obat darurat.",
            "contact": "021-7889001 ext. 500"
        },
    ]

    db = SessionLocal()
    try:
        for svc in dummy:
            es = EmergencyService(
                service_name=svc["service_name"],
                description=svc["description"],
                contact=svc["contact"]
            )
            db.add(es)
        db.commit()
        print(f"✅ Memasukkan {len(dummy)} baris ke emergency_services")
    except Exception as e:
        db.rollback()
        print("❌ Error saat memasukkan data emergency_services:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()
