from src.repository.base_repository import BaseRepository


class AuditRepository(BaseRepository):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AuditRepository, cls).__call__(*args, **kwargs)

        return cls._instance
