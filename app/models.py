from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, Text, BigInteger
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class University(Base):
    __tablename__ = "universities"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    domain = Column(String)

    users = relationship("User", back_populates="university")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id"))
    login_enc = Column(Text, nullable=False)
    password_enc = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    university = relationship("University", back_populates="users")
    settings = relationship("UserSettings", back_populates="user", uselist=False)

class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    daily_digest = Column(Boolean, default=True)
    reminders = Column(Boolean, default=False)
    language = Column(String, default='ru')
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="settings")
