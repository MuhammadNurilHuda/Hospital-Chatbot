# app\session.py

import os
import json
import uuid
import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

# Waktu kedaluwarsa session (dalam detik).
SESSION_EXPIRY = 1800

def create_session(initial_data=None):
    """
    Membuat session baru dengan data awal (optional).
    Mengembalikan session_id yang unik.
    """
    session_id = str(uuid.uuid4())
    data = initial_data if initial_data is not None else {}
    redis_client.setex(session_id, SESSION_EXPIRY, json.dumps(data))
    return session_id

def get_session(session_id):
    """
    Mengembalikan data session (dictionary) berdasarkan session_id.
    Jika session tidak ada atau telah expired, mengembalikan None.
    """
    data = redis_client.get(session_id)
    if data:
        return json.loads(data)
    return None

def update_session(session_id, new_data):
    """
    Memperbarui data session dengan menggabungkan new_data ke data yang sudah ada.
    Mengembalikan session data yang telah diperbarui.
    """
    session_data = get_session(session_id) or {}
    session_data.update(new_data)
    redis_client.setex(session_id, SESSION_EXPIRY, json.dumps(session_data))
    return session_data

def delete_session(session_id):
    """
    Menghapus session berdasarkan session_id.
    """
    redis_client.delete(session_id)