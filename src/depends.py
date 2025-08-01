from config import (
    DB_USER,
    DB_NAME,
    DB_PASSWORD
)
from src.repository import (
    CustomerRepository,
    DealsRepository,
    AuditRepository
)
from src.core.database import DatabaseHandler
from src.tables import (
    Customers,
    Deals,
    Audit
)

database_instance = DatabaseHandler(
    user=DB_USER,
    password=DB_PASSWORD,
    db_name=DB_NAME,
)

customer_repository = CustomerRepository(database_instance=database_instance, table=Customers)
deals_repository = DealsRepository(database_instance=database_instance, table=Deals)
audit_repository = AuditRepository(database_instance=database_instance, table=Audit)
