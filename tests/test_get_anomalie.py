import uuid

from fastapi import status


class TestListAnomalies:
    """Tests for GET /anomalie-adresse endpoint (list all)."""

    def test_list_anomalies_empty(self, client):
        """Test listing when no anomalies exist."""
        response = client.get("/anomalie-adresse")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_anomalies_with_data(self, client, valid_anomalie_data):
        """Test listing after creating anomalies."""
        # Create two anomalies
        client.post("/anomalie-adresse", json=valid_anomalie_data)
        client.post("/anomalie-adresse", json=valid_anomalie_data)

        response = client.get("/anomalie-adresse")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(a["status"] == "ACKNOWLEDGED" for a in data)


class TestGetAnomalie:
    """Tests for GET /anomalie-adresse/{id} endpoint."""

    def test_get_anomalie_success(self, client, valid_anomalie_data):
        """Test successful anomaly retrieval."""
        # Create an anomaly first
        create_response = client.post("/anomalie-adresse", json=valid_anomalie_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        created_id = create_response.json()["id"]

        # Retrieve the anomaly
        response = client.get(f"/anomalie-adresse/{created_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == created_id
        assert data["status"] == "ACKNOWLEDGED"
        assert data["codeOi"] == valid_anomalie_data["codeOi"]
        assert data["codeOc"] == valid_anomalie_data["codeOc"]

    def test_get_anomalie_not_found(self, client):
        """Test retrieval of non-existent anomaly."""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/anomalie-adresse/{fake_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"]["code"] == "NOT_FOUND"

    def test_get_anomalie_invalid_uuid(self, client):
        """Test retrieval with invalid UUID format."""
        response = client.get("/anomalie-adresse/invalid-uuid")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_get_anomalie_preserves_all_fields(self, client, valid_anomalie_data):
        """Test that all fields are preserved after creation and retrieval."""
        # Create an anomaly
        create_response = client.post("/anomalie-adresse", json=valid_anomalie_data)
        created_id = create_response.json()["id"]

        # Retrieve and verify all fields
        response = client.get(f"/anomalie-adresse/{created_id}")
        data = response.json()

        assert (
            data["building"]["address"]["city"]
            == valid_anomalie_data["building"]["address"]["city"]
        )
        assert (
            data["building"]["address"]["postcode"]
            == valid_anomalie_data["building"]["address"]["postcode"]
        )
        assert (
            data["building"]["address"]["streetName"]
            == valid_anomalie_data["building"]["address"]["streetName"]
        )
        assert data["building"]["name"] == valid_anomalie_data["building"]["name"]
        assert data["externalId"] == valid_anomalie_data["externalId"]
        assert data["priority"] == valid_anomalie_data["priority"]
        assert len(data["relatedEntity"]) == len(valid_anomalie_data["relatedEntity"])
