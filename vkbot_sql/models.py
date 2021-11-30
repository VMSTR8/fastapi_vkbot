import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from vkbot_sql .database import Base


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    link = Column(String, nullable=False, unique=True)
    text = Column(Text, nullable=False, index=True)


class Answers(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(),
                        onupdate=datetime.datetime.utcnow(), nullable=False)
    key = Column(String, nullable=False, unique=True)
    answer = Column(Text, nullable=False)
