from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base =  declarative_base()

class Achivements(Base):
    __tablename__ = 'activity'

    act_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ReportedEvents(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    event_type = Column(String)

class AIAdvice(Base):
    __tablename__ = "usermood"

    id = Column(Integer, primary_key=True, index=True)
    user_say = Column(String)



