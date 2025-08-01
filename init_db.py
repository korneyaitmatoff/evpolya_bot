from src.depends import database_instance
from src.tables import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=database_instance.engine)
