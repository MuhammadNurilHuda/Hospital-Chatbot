import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primery_key=True, index=True)
    name = Column(String(100))
    phone = Column(String(15))
    doctor_specialist = Column(String(100))
    appointment_date = Column(Date)

Base.metadata.create_all(bind=engine)