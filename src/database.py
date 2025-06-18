from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import (
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
)
from src.tables import (
    Base,
    Customers,
    Deals
)

engine = create_engine(
    url=f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
)


def add_row(table: Base, **kwargs):
    session = Session(bind=engine)
    session.add(table(**kwargs))
    session.commit()


def set_success_deals(customer_id: int):
    session = Session(bind=engine)
    session.query(Deals).filter(
        Deals.customer_telegram_id == customer_id,
    ).update(values={"is_success": True})
    session.commit()


def set_expired_date(months: int, customer_telegram_id: int):
    dt = datetime.now() + relativedelta(months=months)
    session = Session(bind=engine)
    session.query(Customers).filter(
        Customers.telegram_id == customer_telegram_id,
    ).update(values={"expired_at": dt})
    session.commit()


def get_deal_by_customer_telegram_id(customer_telegram_id: int):
    session = Session(bind=engine)

    data = session.query(Deals).filter(
        Deals.customer_telegram_id == customer_telegram_id,
    ).order_by(Deals.id.desc()).first()

    session.close()

    return data


def get_active_user(customer_telegram_id: int):
    session = Session(bind=engine)

    data = session.query(Customers).filter(
        Customers.telegram_id == customer_telegram_id,
        Customers.expired_at >= datetime.now(),
    ).first()

    session.close()

    return data


def set_chat_id(customer_telegram_id: int, chat_id: int):
    session = Session(bind=engine)
    session.query(Customers).filter(
        Customers.telegram_id == customer_telegram_id,
    ).update(values={"chat_id": chat_id})
    session.commit()
