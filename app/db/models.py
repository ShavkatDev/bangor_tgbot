from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, BigInteger, Date, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.db.database import Base
import datetime

class University(Base):
    __tablename__ = "university"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="university")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    university_id = Column(Integer, ForeignKey("university.id"))
    group_id = Column(Integer, index=True, nullable=False)
    inet_id = Column(Integer, nullable=True)
    semester_id = Column(Integer, nullable=True)
    student_id = Column(Text, nullable=False)
    password_inet = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    university = relationship("University", back_populates="users")
    settings = relationship("UserSettings", back_populates="user", uselist=False)

class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    daily_digest = Column(Boolean, default=True)
    today_schedule_digest = Column(Boolean, default=True)
    language = Column(String, default='en')
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="settings")

class ScheduleCache(Base):
    __tablename__ = "schedule_cache"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    data = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
