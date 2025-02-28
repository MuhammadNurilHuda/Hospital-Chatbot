# app\main.py

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from app.chatbot import get_response
from sqlalchemy.orm import Session
from app.database import SessionLocal. Appointment

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = get_response(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Hospital Chatbot API is running!"}
