import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage.memory import storage


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    """Clear storage before each test."""
    storage.clear()
    yield
    storage.clear()


@pytest.fixture
def valid_anomalie_data():
    """Valid anomaly creation data."""
    return {
        "codeOi": "AXIONE",
        "codeOc": "ORANGE",
        "@type": "AnomalieAdresseCreation",
        "building": {
            "address": {
                "city": "Paris",
                "postcode": "75001",
                "streetName": "Rue de Rivoli",
                "streetNr": "123",
                "streetType": "rue",
            },
            "name": "Immeuble Test",
            "housingsNumber": 10,
        },
        "relatedEntity": [{"id": "REF-001", "role": "building", "@referredType": "Building"}],
        "externalId": "OC-REF-12345",
        "priority": "HIGH",
    }


@pytest.fixture
def minimal_anomalie_data():
    """Minimal valid anomaly creation data (only required fields)."""
    return {
        "codeOi": "AXIONE",
        "codeOc": "SFR",
        "@type": "AnomalieAdresseNewBuilding",
        "building": {
            "address": {"city": "Lyon", "postcode": "69001", "streetName": "Place Bellecour"}
        },
        "relatedEntity": [{"id": "REF-002"}],
    }
