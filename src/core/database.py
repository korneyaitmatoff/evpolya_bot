from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.tables import Base


class DatabaseHandler:
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseHandler, cls).__call__(*args, **kwargs)

        return cls._instance

    def __init__(self, user: str, password: str, db_name: str):
        self.engine = create_engine(
            url=f"postgresql+psycopg2://{user}:{password}@localhost:5432/{db_name}"
        )

    def __enter__(self):
        self.session = Session(bind=self.engine)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def add_row(self, table: Base, **kwargs):
        session = Session(bind=self.engine)
        session.add(table(**kwargs))
        session.commit()
