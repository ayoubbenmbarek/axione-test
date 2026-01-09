from enum import Enum


class AnomalieStatus(str, Enum):
    """Status of an address anomaly - simplified for this test."""

    ACKNOWLEDGED = "ACKNOWLEDGED"
    CANCELED = "CANCELED"


class AnomalieType(str, Enum):
    """Type of address anomaly as defined by Interop specification."""

    CREATION = "AnomalieAdresseCreation"
    NEW_BUILDING = "AnomalieAdresseNewBuilding"
    UPDATE_IMB = "AnomalieAdresseUpdateImb"
    UPDATE_NB_LOGEMENTS = "AnomalieAdresseUpdateNbLogements"


class Priority(str, Enum):
    """Priority level for anomaly processing."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
