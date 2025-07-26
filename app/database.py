# app/database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.logging import logger

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
logger.info(f"Menghubungkan ke database dengan url: {DB_URL}")

engine = (
    create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)
    if DB_URL.startswith("sqlite")
    else create_engine(DB_URL, echo=True)
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()