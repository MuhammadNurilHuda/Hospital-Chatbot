# app\main.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date

from app.database import SessionLocal, Appointment, UserActivityLog
from app.chatbot import get_response
from app.logging import logger

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    message: str

class AppointmentRequest(BaseModel):
    name: str
    phone: str
    doctor_specialist: str
    appointment_date: date

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tabel database berhasil dibuat atau sudah ada.")
except Exception as e:
    logger.error("Gagal membuat tabel database", exc_info=True)

@app.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        logger.info("Menerima request chat.")
        response_text = get_response(request.message)
        logger.debug(f"Response dari chatbot {response_text}")

        user_log = UserActivityLog(prompt=request.message, response=response_text)
        db.add(user_log)
        db.commit()
        db.refresh(user_log)

        logger.info(f"User activity logged dengan id: {user_log.id}")

        return {"response": response_text}
    except Exception as e:
        logger.error(f"Error pada endpoint /chat", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/appointment/book")
def book_appointment(request: AppointmentRequest, db: Session=Depends(get_db)):
    try:
        logger.info("Menerima booking appointment.")
        new_appointment = Appointment(
            name=request.name,
            phone=request.phone,
            doctor_specialist=request.doctor_specialist,
            appointment_date=request.appointment_date
        )

        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        logger.info(f"Appointment berhasil dibuat dengan ID: {new_appointment.id}")
        return {"message":"Appointment booked succesfully", "appointment_id":new_appointment.id}
    
    except Exception as e:
        logger.error("Error pada endpoint /appointment/book", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    logger.info("Endpoint root diakses.")
    return {"message": "Hospital Chatbot API is running!"}
