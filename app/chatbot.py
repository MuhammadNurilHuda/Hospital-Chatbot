# app\chatbot.py

import os
from openai import OpenAI
from dotenv import load_dotenv
from app.logging import logger

# Kata kunci booking
BOOKING_KEYWORDS = ["booking", "buat janji", "reservasi", "pesan dokter"]


load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

def get_response(user_input: str):
    logger.info(f"Menerima input dari user: {user_input}")
    if any(keyword in user_input.lower() for keyword in BOOKING_KEYWORDS):
        response = "Tentu! Silakan berikan informasi berikut:\n- Nama Lengkap\n- Nomor HP\n- Spesialis Dokter yang Anda butuhkan\n- Jadwal yang diinginkan"
        logger.debug("Mendeteksi intent booking, memberikan instruksi booking.")
        return response

    try:
        response_obj = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": user_input}]
        )
        response_text = response_obj.choices[0].message.content
        logger.debug(f"Respons dari API: {response_text}")
        return response_text

    except Exception as e:
        logger.error(e)
        raise