from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

# Use "db" for Docker, "localhost" for local Windows testing
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/khmer_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionHistory(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text)
    prediction_output = Column(Text) 
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# THIS IS THE FUNCTION THE ERROR IS MISSING:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()