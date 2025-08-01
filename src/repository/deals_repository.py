from src.repository.base_repository import BaseRepository
from src.tables import Deals


class DealsRepository(BaseRepository):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DealsRepository, cls).__call__(*args, **kwargs)

        return cls._instance

    def set_success_deals(self, customer_id: int):
        """Set success result for deal

        Args:
            customer_id:
        """
        with self.database_instance as inst:
            inst.session.query(Deals).filter(
                Deals.customer_telegram_id == customer_id,
            ).update(values={"is_success": True})
            inst.session.commit()

    def get_deal_by_customer_telegram_id(self, customer_telegram_id: int):
        """Get deal from db by customer's telegram id

        Args:
            customer_telegram_id:
        """
        with self.database_instance as inst:
            data = inst.session.query(Deals).filter(
                Deals.customer_telegram_id == customer_telegram_id,
            ).order_by(Deals.id.desc()).first()

        return data
