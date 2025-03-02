# app\main.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from app.chatbot import get_response
from sqlalchemy.orm import Session
from app.database import SessionLocal, Appointment
from datetime import date

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
        response = get_response(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/appointment/book")
def book_appointment(request: AppointmentRequest, db: Session=Depends(get_db)):
    new_appointment = Appointment(
        name=request.name,
        phone=request.phone,
        doctor_specialist=request.doctor_specialist,
        appointment_date=request.appointment_date
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return {"message":"Appointment booked succesfully", "appointment_id":new_appointment.id}

@app.get("/")
def root():
    return {"message": "Hospital Chatbot API is running!"}
