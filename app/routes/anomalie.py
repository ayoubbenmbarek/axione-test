"""Routes pour la gestion des anomalies d'adresse."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.models import (
    AnomalieAdresse,
    AnomalieAdresseCreate,
    AnomalieAdresseUpdate,
    AnomalieStatus,
    ErrorResponse,
)
from app.services.anomalie import (
    AnomalieNotFoundError,
    InvalidTransitionError,
    cancel_anomalie,
    create_anomalie,
    get_anomalie,
)

router = APIRouter(prefix="/anomalie-adresse", tags=["Anomalie Adresse"])


@router.get(
    "",
    response_model=list[AnomalieAdresse],
    summary="Lister toutes les anomalies",
    description="Récupérer la liste de toutes les anomalies en mémoire (debug).",
    responses={
        200: {"description": "Liste des anomalies"},
    },
)
async def list_anomalies_endpoint() -> list[AnomalieAdresse]:
    """Lister toutes les anomalies stockées en mémoire."""
    from app.storage.memory import storage

    # Debug: print to server console
    print(f"\n[DEBUG] Storage contains {len(storage._anomalies)} anomalies:")
    for uid, anomalie in storage._anomalies.items():
        print(f"  - {uid}: {anomalie.status} ({anomalie.code_oc})")
    print()

    return storage.list_all()


@router.post(
    "",
    response_model=AnomalieAdresse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une anomalie d'adresse",
    description=(
        "Créer une nouvelle anomalie d'adresse. "
        "L'anomalie est immédiatement créée avec le statut ACKNOWLEDGED."
    ),
    responses={
        201: {"description": "Anomalie créée avec succès"},
        400: {"description": "Corps de requête invalide", "model": ErrorResponse},
    },
)
async def create_anomalie_endpoint(data: AnomalieAdresseCreate) -> AnomalieAdresse:
    """Créer une nouvelle anomalie d'adresse."""
    return create_anomalie(data)


@router.get(
    "/{anomalie_id}",
    response_model=AnomalieAdresse,
    summary="Récupérer une anomalie d'adresse",
    description="Récupérer une anomalie d'adresse par son identifiant unique.",
    responses={
        200: {"description": "Anomalie récupérée avec succès"},
        404: {"description": "Anomalie non trouvée", "model": ErrorResponse},
    },
)
async def get_anomalie_endpoint(anomalie_id: UUID) -> AnomalieAdresse:
    """Récupérer une anomalie d'adresse par son ID."""
    try:
        return get_anomalie(anomalie_id)
    except AnomalieNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "reason": str(e),
                "message": f"No anomaly found with id {anomalie_id}",
            },
        ) from e


@router.patch(
    "/{anomalie_id}",
    response_model=AnomalieAdresse,
    summary="Mettre à jour le statut d'une anomalie",
    description=(
        "Mettre à jour le statut d'une anomalie d'adresse. "
        "Seule la transition ACKNOWLEDGED → CANCELED est autorisée."
    ),
    responses={
        200: {"description": "Anomalie mise à jour avec succès"},
        404: {"description": "Anomalie non trouvée", "model": ErrorResponse},
        409: {"description": "Transition de statut invalide", "model": ErrorResponse},
    },
)
async def update_anomalie_endpoint(
    anomalie_id: UUID, data: AnomalieAdresseUpdate
) -> AnomalieAdresse:
    """Mettre à jour le statut d'une anomalie (annulation)."""
    # Only CANCELED status is allowed in this simplified version
    if data.status != AnomalieStatus.CANCELED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_STATUS",
                "reason": "Only CANCELED status is allowed for updates",
                "message": f"Cannot update to status {data.status.value}",
            },
        )

    try:
        return cancel_anomalie(anomalie_id)
    except AnomalieNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "reason": str(e),
                "message": f"No anomaly found with id {anomalie_id}",
            },
        ) from e
    except InvalidTransitionError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "INVALID_TRANSITION",
                "reason": str(e),
                "message": (
                    f"Cannot transition from {e.current_status.value} to {e.target_status.value}"
                ),
            },
        ) from e
