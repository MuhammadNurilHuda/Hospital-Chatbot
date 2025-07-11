# app\database.py

import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine, Column, 
    Integer, String, Date, 
    Text, DateTime)
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone
from app.logging import logger

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
logger.info(f"Menghubungkan ke database dengan url: {DB_URL}")

if DB_URL.startswith("sqlite"):
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
else:
    engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    phone = Column(String(15))
    doctor_specialist = Column(String(100))
    appointment_date = Column(Date)

class UserActivityLog(Base):
    __tablename__ = "user_activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Berhasil membuat tabel database")

except Exception as e:
    logger.error("Gagal membuat database", exc_info=True)