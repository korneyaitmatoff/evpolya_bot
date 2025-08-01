from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    TIMESTAMP,
    Boolean
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    telegram_id = Column(BigInteger)
    chat_id = Column(BigInteger, default=0)
    expired_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.now())


class Deals(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True)
    customer_telegram_id = Column(BigInteger)
    service_months = Column(Integer)
    is_success = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.now())


class Audit(Base):
    __tablename__ = "audit"

    id = Column(Integer, primary_key=True)
    user_telegram_id = Column(BigInteger)
    chat_id = Column(BigInteger)
    fullname = Column(String)
    username = Column(String)
    event_name = Column(String)
    description = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.now())
