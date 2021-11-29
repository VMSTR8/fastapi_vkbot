import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    link = Column(String, nullable=False, unique=True)
    text = Column(Text, nullable=False, unique=True, index=True)


class Answers(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                        onupdate=datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), nullable=False)
    key = Column(String, nullable=False, unique=True)
    answer = Column(Text, nullable=False)
