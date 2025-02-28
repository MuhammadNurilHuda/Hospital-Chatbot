# app\main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/chat")
async def chat(request: ChatRequest):
    response = await get_response(request.message)
    return {"response": response}