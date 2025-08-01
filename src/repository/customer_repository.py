from datetime import datetime

from dateutil.relativedelta import relativedelta

from src.repository.base_repository import BaseRepository
from src.tables import Customers


class CustomerRepository(BaseRepository):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CustomerRepository, cls).__call__(*args, **kwargs)

        return cls._instance

    def set_expired_date(self, months: int = 0, customer_telegram_id: int = 0, expired_date: datetime = None):
        dt = (datetime.now() + relativedelta(months=months)) if expired_date is None else expired_date

        with self.database_instance as inst:
            inst.session.query(Customers).filter(
                Customers.telegram_id == customer_telegram_id,
            ).update(values={"expired_at": dt})

            inst.session.commit()

    def get_active_user(self, customer_telegram_id: int):
        """Get user with non-expired subscribe

        Args:
            customer_telegram_id:
        """
        with self.database_instance as inst:
            data = inst.session.query(Customers).filter(
                Customers.telegram_id == customer_telegram_id,
                Customers.expired_at >= datetime.now(),
            ).first()

        return data

    def set_chat_id(self, customer_telegram_id: int, chat_id: int):
        """Update customer row and set chat id

        Args:
            customer_telegram_id:
            chat_id:
        """
        with self.database_instance as inst:
            inst.session.query(Customers).filter(
                Customers.telegram_id == customer_telegram_id,
            ).update(values={"chat_id": chat_id})
            inst.session.commit()

    def get_customer_by_telegram_id(self, customer_telegram_id: int):
        """Get customer by telegram id

        Args:
            customer_telegram_id:
        """
        with self.database_instance as inst:
            data = inst.session.query(Customers).filter(
                Customers.telegram_id == customer_telegram_id,
            ).first()

        return data

    def get_expired_customers(self) -> list:
        with self.database_instance as inst:
            return inst.session.query(Customers).filter(
                Customers.expired_at < datetime.now()
            ).all()
