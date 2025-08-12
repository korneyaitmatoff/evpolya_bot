from src.core.database import DatabaseHandler
from src.tables import Base


class BaseRepository:
    def __init__(self, database_instance: DatabaseHandler, table: Base):
        self.database_instance = database_instance
        self.table = table

    def add_row(self, **kwargs):
        with self.database_instance as session:
            session.add_row(table=self.table, **kwargs)
