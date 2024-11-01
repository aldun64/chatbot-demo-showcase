from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# User model
# CURRENTLY UNUSED
class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    sessions = relationship("Transcript", back_populates="user")

class Transcript(Base):
    __tablename__ = 'transcripts'
    
    transcript_id = Column(Integer, primary_key=True, index=True)
    interview_date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User", back_populates="sessions")
