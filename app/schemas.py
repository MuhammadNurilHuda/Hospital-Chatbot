# app/schemas.py
from pydantic import BaseModel
from datetime import time
from typing import List

class DoctorScheduleSchema(BaseModel):
    id: int
    doctor_name: str
    specialty: str
    available_days: str
    start_time: time
    end_time: time

    class Config:
        # Untuk SQLAlchemy ORM objects
        from_attributes = True
