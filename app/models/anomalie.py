from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .enums import AnomalieStatus, AnomalieType, Priority


class GeographicAddress(BaseModel):
    """Geographic address following Interop specification."""

    model_config = ConfigDict(populate_by_name=True)

    city: str = Field(..., min_length=1, description="City name")
    postcode: str = Field(
        ..., min_length=5, max_length=5, pattern=r"^\d{5}$", description="Postal code (5 digits)"
    )
    street_name: str = Field(..., alias="streetName", min_length=1, description="Street name")
    street_nr: str | None = Field(None, alias="streetNr", description="Street number")
    street_type: str | None = Field(
        None, alias="streetType", description="Street type (rue, avenue, etc.)"
    )
    code_insee: str | None = Field(
        None, alias="codeInsee", pattern=r"^\d{5}$", description="INSEE code"
    )


class Building(BaseModel):
    """Building information following Interop specification."""

    model_config = ConfigDict(populate_by_name=True)

    address: GeographicAddress = Field(..., description="Geographic address of the building")
    name: str | None = Field(None, description="Building name")
    housings_number: int | None = Field(
        None, alias="housingsNumber", ge=0, description="Number of housing units"
    )
    new_construction: bool | None = Field(
        None, alias="newConstruction", description="Whether this is a new construction"
    )


class RelatedEntity(BaseModel):
    """Related entity reference following Interop specification."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., min_length=1, description="Entity identifier")
    role: str = Field(default="building", description="Role of the related entity")
    referred_type: str = Field(
        default="Building", alias="@referredType", description="Type of the referred entity"
    )


class AnomalieAdresseCreate(BaseModel):
    """Request model for creating an address anomaly."""

    model_config = ConfigDict(populate_by_name=True)

    code_oi: str = Field(
        ..., alias="codeOi", min_length=1, description="Infrastructure Operator code"
    )
    code_oc: str = Field(..., alias="codeOc", min_length=1, description="Commercial Operator code")
    type: AnomalieType = Field(..., alias="@type", description="Type of anomaly")
    building: Building = Field(..., description="Building information")
    related_entity: list[RelatedEntity] = Field(
        ...,
        alias="relatedEntity",
        min_length=1,
        description="Related entities (at least one required)",
    )
    external_id: str | None = Field(
        None, alias="externalId", description="External reference ID from OC"
    )
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")


class AnomalieAdresse(BaseModel):
    """Complete address anomaly model (response)."""

    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(..., description="Unique identifier")
    status: AnomalieStatus = Field(..., description="Current status")
    created_date: datetime = Field(..., alias="createdDate", description="Creation timestamp")
    code_oi: str = Field(..., alias="codeOi", description="Infrastructure Operator code")
    code_oc: str = Field(..., alias="codeOc", description="Commercial Operator code")
    type: AnomalieType = Field(..., alias="@type", description="Type of anomaly")
    building: Building = Field(..., description="Building information")
    related_entity: list[RelatedEntity] = Field(
        ..., alias="relatedEntity", description="Related entities"
    )
    external_id: str | None = Field(
        None, alias="externalId", description="External reference ID from OC"
    )
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")


class AnomalieAdresseUpdate(BaseModel):
    """Request model for updating an address anomaly (cancel)."""

    status: AnomalieStatus = Field(..., description="Target status (only CANCELED allowed)")


class ErrorResponse(BaseModel):
    """Standard error response."""

    code: str = Field(..., description="Error code")
    reason: str = Field(..., description="Human-readable error reason")
    message: str | None = Field(None, description="Detailed error message")
