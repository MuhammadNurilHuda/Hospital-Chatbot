# app\chatbot.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Kata kunci booking
BOOKING_KEYWORDS = ["booking", "buat janji", "reservasi", "pesan dokter"]


load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

def get_response(user_input: str):
    if any(keyword in user_input.lower() for keyword in BOOKING_KEYWORDS):
        return "Tentu! Silakan berikan informasi berikut:\n- Nama Lengkap\n- Nomor HP\n- Spesialis Dokter yang Anda butuhkan\n- Jadwal yang diinginkan"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content
