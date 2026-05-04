from typing import List

class NotificationHistory:
    """Historial de notificaciones en memoria."""

    def __init__(self):
        self._records: List[dict] = []

    def save(self, record) -> None:
        self._records.append(record.model_dump())

    def all(self) -> List[dict]:
        return list(self._records)
