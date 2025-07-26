# app\models.py

from sqlalchemy import Column, Integer, String, Time, Text, Date
from .database import Base


class DoctorSchedule(Base):
    __tablename__ = "doctors_schedule"

    id = Column(Integer, primary_key=True, index=True)
    doctor_name    = Column(String, nullable=False)
    specialty      = Column(String, nullable=False)
    available_days = Column(String, nullable=False)
    start_time     = Column(Time, nullable=False)
    end_time       = Column(Time, nullable=False)


class Appointment(Base):
    __tablename__ = "appointments"

    id                = Column(Integer, primary_key=True, index=True)
    name              = Column(String(100), nullable=False)
    phone             = Column(String(15),  nullable=False)
    doctor_specialist = Column(String(100), nullable=False)
    appointment_date  = Column(Date,         nullable=False)


class UserActivityLog(Base):
    __tablename__ = "user_activity_logs"
    
    id        = Column(Integer, primary_key=True, index=True)
    prompt    = Column(Text,     nullable=False)
    response  = Column(Text,     nullable=False)
    timestamp = Column(Date)


class HospitalFAQ(Base):
    __tablename__ = "hospital_faq"

    id       = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)
    answer   = Column(Text, nullable=False)


class HospitalLocation(Base):
    __tablename__ = "hospital_locations"

    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    phone   = Column(String(50), nullable=False)


class AppointmentProcess(Base):
    __tablename__ = "appointment_process"

    id          = Column(Integer, primary_key=True, index=True)
    step_order  = Column(Integer, nullable=False)
    title       = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)


class EmergencyService(Base):
    __tablename__ = "emergency_services"

    id           = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), nullable=False)
    description  = Column(Text, nullable=False)
    contact      = Column(String(50), nullable=False)
