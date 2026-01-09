from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.models import (
    AnomalieAdresse,
    AnomalieAdresseCreate,
    AnomalieStatus,
)
from app.storage.memory import storage


class InvalidTransitionError(Exception):
    """Raised when a status transition is not allowed."""

    def __init__(self, current_status: AnomalieStatus, target_status: AnomalieStatus):
        self.current_status = current_status
        self.target_status = target_status
        super().__init__(f"Invalid transition from {current_status.value} to {target_status.value}")


class AnomalieNotFoundError(Exception):
    """Raised when an anomaly is not found."""

    def __init__(self, anomalie_id: UUID):
        self.anomalie_id = anomalie_id
        super().__init__(f"Anomaly with id {anomalie_id} not found")


# Valid status transitions (simplified for this test)
VALID_TRANSITIONS: dict[AnomalieStatus, list[AnomalieStatus]] = {
    AnomalieStatus.ACKNOWLEDGED: [AnomalieStatus.CANCELED],
    AnomalieStatus.CANCELED: [],  # Terminal state
}


def can_transition(current: AnomalieStatus, target: AnomalieStatus) -> bool:
    """Check if a status transition is allowed."""
    allowed = VALID_TRANSITIONS.get(current, [])
    return target in allowed


def create_anomalie(data: AnomalieAdresseCreate) -> AnomalieAdresse:
    """Create a new anomaly with ACKNOWLEDGED status."""
    anomalie = AnomalieAdresse(
        id=uuid4(),
        status=AnomalieStatus.ACKNOWLEDGED,
        created_date=datetime.now(timezone.utc),
        code_oi=data.code_oi,
        code_oc=data.code_oc,
        type=data.type,
        building=data.building,
        related_entity=data.related_entity,
        external_id=data.external_id,
        priority=data.priority,
    )
    return storage.create(anomalie)


def get_anomalie(anomalie_id: UUID) -> AnomalieAdresse:
    """Retrieve an anomaly by ID."""
    anomalie = storage.get(anomalie_id)
    if anomalie is None:
        raise AnomalieNotFoundError(anomalie_id)
    return anomalie


def cancel_anomalie(anomalie_id: UUID) -> AnomalieAdresse:
    """Cancel an anomaly (transition to CANCELED status)."""
    anomalie = storage.get(anomalie_id)
    if anomalie is None:
        raise AnomalieNotFoundError(anomalie_id)

    target_status = AnomalieStatus.CANCELED

    if not can_transition(anomalie.status, target_status):
        raise InvalidTransitionError(anomalie.status, target_status)

    # Create updated anomalie with new status
    updated_anomalie = anomalie.model_copy(update={"status": target_status})
    return storage.update(updated_anomalie)
