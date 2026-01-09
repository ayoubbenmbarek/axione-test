from uuid import UUID

from app.models import AnomalieAdresse


class InMemoryStorage:
    """In-memory storage for anomalies using a dictionary."""

    def __init__(self) -> None:
        self._anomalies: dict[UUID, AnomalieAdresse] = {}

    def create(self, anomalie: AnomalieAdresse) -> AnomalieAdresse:
        """Store a new anomaly."""
        self._anomalies[anomalie.id] = anomalie
        return anomalie

    def get(self, anomalie_id: UUID) -> AnomalieAdresse | None:
        """Retrieve an anomaly by ID."""
        return self._anomalies.get(anomalie_id)

    def update(self, anomalie: AnomalieAdresse) -> AnomalieAdresse:
        """Update an existing anomaly."""
        self._anomalies[anomalie.id] = anomalie
        return anomalie

    def delete(self, anomalie_id: UUID) -> bool:
        """Delete an anomaly by ID."""
        if anomalie_id in self._anomalies:
            del self._anomalies[anomalie_id]
            return True
        return False

    def list_all(self) -> list[AnomalieAdresse]:
        """List all anomalies."""
        return list(self._anomalies.values())

    def clear(self) -> None:
        """Clear all anomalies (useful for testing)."""
        self._anomalies.clear()


# Singleton instance
storage = InMemoryStorage()
