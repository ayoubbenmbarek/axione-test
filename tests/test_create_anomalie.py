from fastapi import status


class TestCreateAnomalie:
    """Tests for POST /anomalie-adresse endpoint."""

    def test_create_anomalie_success(self, client, valid_anomalie_data):
        """Test successful anomaly creation."""
        response = client.post("/anomalie-adresse", json=valid_anomalie_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        # Check required response fields
        assert "id" in data
        assert data["status"] == "ACKNOWLEDGED"
        assert "createdDate" in data
        assert data["codeOi"] == valid_anomalie_data["codeOi"]
        assert data["codeOc"] == valid_anomalie_data["codeOc"]
        assert data["@type"] == valid_anomalie_data["@type"]

    def test_create_anomalie_minimal_data(self, client, minimal_anomalie_data):
        """Test anomaly creation with minimal required fields."""
        response = client.post("/anomalie-adresse", json=minimal_anomalie_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "ACKNOWLEDGED"
        assert data["priority"] == "MEDIUM"  # Default value

    def test_create_anomalie_missing_code_oi(self, client, valid_anomalie_data):
        """Test anomaly creation fails without codeOi."""
        del valid_anomalie_data["codeOi"]
        response = client.post("/anomalie-adresse", json=valid_anomalie_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_anomalie_missing_code_oc(self, client, valid_anomalie_data):
        """Test anomaly creation fails without codeOc."""
        del valid_anomalie_data["codeOc"]
        response = client.post("/anomalie-adresse", json=valid_anomalie_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_anomalie_missing_type(self, client, valid_anomalie_data):
        """Test anomaly creation fails without @type."""
        del valid_anomalie_data["@type"]
        response = client.post("/anomalie-adresse", json=valid_anomalie_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_anomalie_invalid_type(self, client, valid_anomalie_data):
        """Test anomaly creation fails with invalid @type."""
        valid_anomalie_data["@type"] = "InvalidType"
        response = client.post("/anomalie-adresse", json=valid_anomalie_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_anomalie_missing_building(self, client, valid_anomalie_data):
        """Test anomaly creation fails without building."""
        del valid_anomalie_data["building"]
        response = client.post("/anomalie-adresse", json=valid_anomalie_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_anomalie_missing_related_entity(self, client, valid_anomalie_data):
        """Test anomaly creation fails without relatedEntity."""
        del valid_anomalie_data["relatedEntity"]
        response = client.post("/anomalie-adresse", json=valid_anomalie_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_anomalie_empty_related_entity(self, client, valid_anomalie_data):
        """Test anomaly creation fails with empty relatedEntity list."""
        valid_anomalie_data["relatedEntity"] = []
        response = client.post("/anomalie-adresse", json=valid_anomalie_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_anomalie_invalid_postcode(self, client, valid_anomalie_data):
        """Test anomaly creation fails with invalid postcode."""
        valid_anomalie_data["building"]["address"]["postcode"] = "123"  # Too short
        response = client.post("/anomalie-adresse", json=valid_anomalie_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_anomalie_all_types(self, client, valid_anomalie_data):
        """Test anomaly creation with all valid @type values."""
        types = [
            "AnomalieAdresseCreation",
            "AnomalieAdresseNewBuilding",
            "AnomalieAdresseUpdateImb",
            "AnomalieAdresseUpdateNbLogements",
        ]

        for anomalie_type in types:
            valid_anomalie_data["@type"] = anomalie_type
            response = client.post("/anomalie-adresse", json=valid_anomalie_data)
            assert response.status_code == status.HTTP_201_CREATED
            assert response.json()["@type"] == anomalie_type
