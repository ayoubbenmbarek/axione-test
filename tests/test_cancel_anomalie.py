import uuid

from fastapi import status


class TestCancelAnomalie:
    """Tests for PATCH /anomalie-adresse/{id} endpoint."""

    def test_cancel_anomalie_success(self, client, valid_anomalie_data):
        """Test successful anomaly cancellation."""
        # Create an anomaly first
        create_response = client.post("/anomalie-adresse", json=valid_anomalie_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        created_id = create_response.json()["id"]

        # Cancel the anomaly
        response = client.patch(f"/anomalie-adresse/{created_id}", json={"status": "CANCELED"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == created_id
        assert data["status"] == "CANCELED"

    def test_cancel_anomalie_not_found(self, client):
        """Test cancellation of non-existent anomaly."""
        fake_id = str(uuid.uuid4())
        response = client.patch(f"/anomalie-adresse/{fake_id}", json={"status": "CANCELED"})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"]["code"] == "NOT_FOUND"

    def test_cancel_anomalie_already_canceled(self, client, valid_anomalie_data):
        """Test cancellation of already canceled anomaly (invalid transition)."""
        # Create and cancel an anomaly
        create_response = client.post("/anomalie-adresse", json=valid_anomalie_data)
        created_id = create_response.json()["id"]

        client.patch(f"/anomalie-adresse/{created_id}", json={"status": "CANCELED"})

        # Try to cancel again
        response = client.patch(f"/anomalie-adresse/{created_id}", json={"status": "CANCELED"})

        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert data["detail"]["code"] == "INVALID_TRANSITION"

    def test_cancel_anomalie_invalid_status(self, client, valid_anomalie_data):
        """Test update with invalid status value."""
        create_response = client.post("/anomalie-adresse", json=valid_anomalie_data)
        created_id = create_response.json()["id"]

        # Try to update with ACKNOWLEDGED (not allowed)
        response = client.patch(f"/anomalie-adresse/{created_id}", json={"status": "ACKNOWLEDGED"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data["detail"]["code"] == "INVALID_STATUS"

    def test_cancel_anomalie_invalid_uuid(self, client):
        """Test cancellation with invalid UUID format."""
        response = client.patch("/anomalie-adresse/invalid-uuid", json={"status": "CANCELED"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_cancel_anomalie_missing_status(self, client, valid_anomalie_data):
        """Test update without status field."""
        create_response = client.post("/anomalie-adresse", json=valid_anomalie_data)
        created_id = create_response.json()["id"]

        response = client.patch(f"/anomalie-adresse/{created_id}", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_cancel_anomalie_unknown_status_value(self, client, valid_anomalie_data):
        """Test update with unknown status value."""
        create_response = client.post("/anomalie-adresse", json=valid_anomalie_data)
        created_id = create_response.json()["id"]

        response = client.patch(
            f"/anomalie-adresse/{created_id}", json={"status": "UNKNOWN_STATUS"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


class TestHealthEndpoint:
    """Tests for GET /health endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "healthy"}
