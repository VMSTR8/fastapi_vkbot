import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Computed, Index

from vkbot_sql .database import Base
from vkbot_sql.tsvector import TSVector


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    link = Column(String, nullable=False, unique=True)
    text = Column(Text, nullable=False, index=True)

    __ts_vector__ = Column(TSVector(), Computed(
        "to_tsvector('english', text)",
        persisted=True))
    __table_args__ = (Index('ix_items___ts_vector__',
                            __ts_vector__, postgresql_using='gin'),)


class Answers(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(),
                        onupdate=datetime.datetime.utcnow(), nullable=False)
    key = Column(String, nullable=False, unique=True)
    answer = Column(Text, nullable=False)
