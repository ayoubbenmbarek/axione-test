from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.anomalie import router as anomalie_router

app = FastAPI(
    title="API Anomalie Adresse",
    description="""
API de gestion des anomalies d'adresse conforme à la spécification Interop Fibre.

## Présentation
Cette API permet aux Opérateurs Commerciaux (OC) de signaler et gérer des anomalies
d'adresse auprès des Opérateurs d'Infrastructure (OI).

## Endpoints
- **POST /anomalie-adresse** - Créer une nouvelle anomalie d'adresse
- **GET /anomalie-adresse/{id}** - Récupérer une anomalie par son identifiant
- **PATCH /anomalie-adresse/{id}** - Mettre à jour le statut (annulation)

## Flux de statut (Simplifié)
- Création : → ACKNOWLEDGED
- Annulation : ACKNOWLEDGED → CANCELED
    """,
    version="1.0.0",
    contact={
        "name": "Axione",
        "url": "https://www.axione.fr",
    },
    license_info={
        "name": "Proprietary",
    },
    openapi_tags=[
        {
            "name": "Anomalie Adresse",
            "description": "Opérations sur les anomalies d'adresse",
        },
    ],
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(anomalie_router)


@app.get("/health", tags=["Santé"])
async def health_check() -> dict[str, str]:
    """Point de contrôle de santé de l'API."""
    return {"status": "healthy"}
