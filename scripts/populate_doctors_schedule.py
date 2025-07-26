#!/usr/bin/env python3
import datetime
from app.database import SessionLocal, engine, Base
from app.models   import DoctorSchedule

def main():
    Base.metadata.create_all(bind=engine)

    dummy = [
        {"doctor_name":"Dr. Andi Wirawan","specialty":"Cardiology","available_days":"Senin–Jumat","start_time":"08:00:00","end_time":"12:00:00"},
        {"doctor_name":"Dr. Andi Wirawan","specialty":"Cardiology","available_days":"Senin–Jumat","start_time":"13:00:00","end_time":"16:00:00"},
        {"doctor_name":"Dr. Budi Santoso","specialty":"Dermatology","available_days":"Selasa, Kamis","start_time":"09:00:00","end_time":"12:00:00"},
        {"doctor_name":"Dr. Citra Mahendra","specialty":"Pediatrics","available_days":"Senin–Sabtu","start_time":"10:00:00","end_time":"14:00:00"},
        {"doctor_name":"Dr. Dian Pratiwi","specialty":"Neurology","available_days":"Rabu, Jumat","start_time":"14:00:00","end_time":"18:00:00"},
    ]

    db = SessionLocal()
    try:
        for d in dummy:
            sched = DoctorSchedule(
                doctor_name    = d["doctor_name"],
                specialty      = d["specialty"],
                available_days = d["available_days"],
                start_time     = datetime.time.fromisoformat(d["start_time"]),
                end_time       = datetime.time.fromisoformat(d["end_time"]),
            )
            db.add(sched)
        db.commit()
        print(f"✅ Memasukkan baris {len(dummy)} ke doctors_schedule")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()
