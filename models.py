from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    query = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)