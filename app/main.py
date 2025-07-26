# app/main.py

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date, time

from app.database import SessionLocal, Base, engine
from app.models import (
    DoctorSchedule,
    HospitalFAQ,
    HospitalLocation,
    AppointmentProcess,
    EmergencyService,
    Appointment,
    UserActivityLog,
)
from app.chatbot import get_response
from app.logging import logger
from app.session import create_session, get_session, update_session

# Pydantic request bodies
class ChatRequest(BaseModel):
    message: str

class AppointmentRequest(BaseModel):
    name: str
    phone: str
    doctor_specialist: str
    appointment_date: date

    class Config:
        orm_mode = True

# Pydantic response schemas
class DoctorScheduleSchema(BaseModel):
    id: int
    doctor_name: str
    specialty: str
    available_days: str
    start_time: time
    end_time: time

    class Config:
        orm_mode = True

class HospitalFAQSchema(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        orm_mode = True

class HospitalLocationSchema(BaseModel):
    id: int
    name: str
    address: str
    phone: str

    class Config:
        orm_mode = True

class AppointmentProcessSchema(BaseModel):
    id: int
    step_order: int
    title: str
    description: str

    class Config:
        orm_mode = True

class EmergencyServiceSchema(BaseModel):
    id: int
    service_name: str
    description: str
    contact: str

    class Config:
        orm_mode = True

# FastAPI setup
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pastikan tabel-tabel ada sebelum server jalan
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tabel database berhasil dibuat atau sudah ada.")
except Exception:
    logger.error("Gagal membuat tabel database", exc_info=True)

# Root endpoint
@app.get("/")
def root():
    logger.info("Endpoint root diakses.")
    return {"message": "Hospital Chatbot API is running!"}

# Chat endpoint
@app.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    session_id: Optional[str] = Header(None),
):
    """
    Endpoint chat dengan session management dan RAG.
    - Mengembalikan session_id baru jika tidak ada atau expired.
    - Menyimpan user activity log.
    """
    logger.info("➡️  Masuk endpoint chat")
    
    # Kelola session
    if not session_id or not get_session(session_id):
        session_id = create_session({})
        logger.debug(f"Membuat session baru: {session_id}")

    user_input = request.message
    logger.info(f"[Session {session_id}] Menerima input: {user_input}")

    try:
        # Dapatkan respons dari chatbot RAG
        response_text = get_response(user_input, session_id)
        # Update session data jika perlu
        update_session(session_id, {"last_message": user_input, "last_response": response_text})

        # Log aktivitas pengguna ke database
        user_log = UserActivityLog(prompt=user_input, response=response_text)
        db.add(user_log)
        db.commit()
        db.refresh(user_log)
        logger.info(f"User activity logged dengan id: {user_log.id}")

        return {"session_id": session_id, "response": response_text}
    except Exception as e:
        logger.error("Error pada endpoint /chat", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/exit")
def exit_chat(session_id: Optional[str] = Header(None)):
    if session_id:
        delete_session(session_id)
    return {"message":"Session direset. Terima kasih!"}
    
# Appointment booking endpoint
@app.post("/appointment/book")
def book_appointment(
    request: AppointmentRequest,
    db: Session = Depends(get_db)
):
    try:
        logger.info("Menerima booking appointment.")
        new_appointment = Appointment(
            name=request.name,
            phone=request.phone,
            doctor_specialist=request.doctor_specialist,
            appointment_date=request.appointment_date,
        )
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        logger.info(f"Appointment berhasil dibuat dengan ID: {new_appointment.id}")
        return {"message": "Appointment booked successfully", "appointment_id": new_appointment.id}
    except Exception as e:
        logger.error("Error pada endpoint /appointment/book", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Supporting endpoints
@app.get("/doctors_schedule", response_model=List[DoctorScheduleSchema])
def get_doctors_schedule(db: Session = Depends(get_db)):
    return db.query(DoctorSchedule).all()

@app.get("/doctors_schedule/{schedule_id}", response_model=DoctorScheduleSchema)
def get_doctor_schedule(schedule_id: int, db: Session = Depends(get_db)):
    sched = db.get(DoctorSchedule, schedule_id)
    if not sched:
        raise HTTPException(404, "Doctor schedule tidak ditemukan")
    return sched

@app.get("/hospital_faq", response_model=List[HospitalFAQSchema])
def list_faq(db: Session = Depends(get_db)):
    return db.query(HospitalFAQ).all()

@app.get("/hospital_faq/{faq_id}", response_model=HospitalFAQSchema)
def get_faq(faq_id: int, db: Session = Depends(get_db)):
    faq = db.get(HospitalFAQ, faq_id)
    if not faq:
        raise HTTPException(404, "FAQ tidak ditemukan")
    return faq

@app.get("/hospital_locations", response_model=List[HospitalLocationSchema])
def list_locations(db: Session = Depends(get_db)):
    return db.query(HospitalLocation).all()

@app.get("/hospital_locations/{loc_id}", response_model=HospitalLocationSchema)
def get_location(loc_id: int, db: Session = Depends(get_db)):
    loc = db.get(HospitalLocation, loc_id)
    if not loc:
        raise HTTPException(404, "Lokasi tidak ditemukan")
    return loc

@app.get("/appointment_process", response_model=List[AppointmentProcessSchema])
def list_process(db: Session = Depends(get_db)):
    return db.query(AppointmentProcess).order_by(AppointmentProcess.step_order).all()

@app.get("/appointment_process/{step_id}", response_model=AppointmentProcessSchema)
def get_process(step_id: int, db: Session = Depends(get_db)):
    step = db.get(AppointmentProcess, step_id)
    if not step:
        raise HTTPException(404, "Proses appointment tidak ditemukan")
    return step

@app.get("/emergency_services", response_model=List[EmergencyServiceSchema])
def list_emergency(db: Session = Depends(get_db)):
    return db.query(EmergencyService).all()

@app.get("/emergency_services/{svc_id}", response_model=EmergencyServiceSchema)
def get_emergency(svc_id: int, db: Session = Depends(get_db)):
    svc = db.get(EmergencyService, svc_id)
    if not svc:
        raise HTTPException(404, "Layanan darurat tidak ditemukan")
    return svc
