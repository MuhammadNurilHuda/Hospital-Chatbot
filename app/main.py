# app\main.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import date

from app.database import SessionLocal, Appointment
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

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        logger.info("Menerima request chat.")
        response = get_response(request.message)
        logger.debug(f"Response dari chatbot {response}")
        return {"response": response}
    except Exception as e:
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
