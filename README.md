# Anomalie Adresse API

API REST pour la gestion des anomalies d'adresse, conforme à la spécification Interop Fibre.

## Contexte

Cette API permet aux Opérateurs Commerciaux (OC) de signaler et gérer des anomalies d'adresse auprès des Opérateurs d'Infrastructure (OI), conformément au standard [Interop Fibre](https://before-interop.github.io/anomalieAdresse/).

## Fonctionnalités

### Endpoints implémentés

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/anomalie-adresse` | Créer une nouvelle anomalie |
| GET | `/anomalie-adresse/{id}` | Récupérer une anomalie par ID |
| PATCH | `/anomalie-adresse/{id}` | Annuler une anomalie |

### Règles métier (simplifiées)

- **Création** : L'anomalie est créée avec le statut `ACKNOWLEDGED`
- **Annulation** : Seule la transition `ACKNOWLEDGED → CANCELED` est autorisée
- **Transition invalide** : Retourne une erreur 409 Conflict

## Installation

### Prérequis

- Python 3.10+
- pip

### Configuration

```bash
# Cloner le projet
git clone <repository-url>
cd AxioneProject

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Commandes Make

```bash
make help       # Afficher toutes les commandes disponibles
make install    # Installer les dépendances
make dev        # Créer venv et installer les dépendances
make run        # Lancer le serveur API
make test       # Exécuter les tests
make coverage   # Tests avec rapport de couverture
make lint       # Vérifier le code (ruff)
make format     # Formater le code (ruff)
make typecheck  # Vérifier les types (mypy)
make clean      # Nettoyer les fichiers cache
make all        # Lint + typecheck + tests
```

## Utilisation

### Démarrer le serveur

```bash
make run
# ou
uvicorn app.main:app --reload
```

Le serveur démarre sur `http://localhost:8000`

### Documentation API

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **OpenAPI JSON** : http://localhost:8000/openapi.json

### Exemples d'utilisation

#### Créer une anomalie

```bash
curl -X POST http://localhost:8000/anomalie-adresse \
  -H "Content-Type: application/json" \
  -d '{
    "codeOi": "AXIONE",
    "codeOc": "ORANGE",
    "@type": "AnomalieAdresseCreation",
    "building": {
      "address": {
        "city": "Saint Maur",
        "postcode": "94100",
        "streetName": "Rue de docteur roux"
      }
    },
    "relatedEntity": [
      {"id": "REF-001"}
    ]
  }'
```

#### Récupérer une anomalie

```bash
curl http://localhost:8000/anomalie-adresse/{id}
```

#### Annuler une anomalie

```bash
curl -X PATCH http://localhost:8000/anomalie-adresse/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "CANCELED"}'
```

## Tests

### Exécuter les tests

```bash
# Tous les tests
pytest

# Avec couverture de code
pytest --cov=app --cov-report=term-missing

# Avec rapport HTML
pytest --cov=app --cov-report=html
```


## Structure du projet

```
AxioneProject/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application FastAPI
│   ├── models/
│   │   ├── enums.py            # Énumérations (Status, Type, Priority)
│   │   └── anomalie.py         # Modèles Pydantic
│   ├── routes/
│   │   └── anomalie.py         # Endpoints API
│   ├── services/
│   │   └── anomalie.py         # Logique métier
│   └── storage/
│       └── memory.py           # Stockage en mémoire
├── tests/
│   ├── conftest.py             # Fixtures pytest
│   ├── test_create_anomalie.py
│   ├── test_get_anomalie.py
│   └── test_cancel_anomalie.py
├── docs/
│   ├── JIRA_TICKETS.md         # Tickets techniques
    ├── Makefile                    # Commandes utiles
├── requirements.txt
├── pyproject.toml              # Config pytest, ruff, mypy
└── README.md
```

## Technologies

- **FastAPI** - Framework web moderne et performant
- **Pydantic v2** - Validation de données
- **uvicorn** - Serveur ASGI
- **pytest** - Framework de tests
- **pytest-cov** - Couverture de code
- **ruff** - Linter et formateur rapide
- **mypy** - Vérification de types statique

## Stockage en mémoire

Le stockage utilise un dictionnaire Python en mémoire.

## Spécification Interop

Cette API est alignée sur la spécification Interop Fibre :
- [Swagger](https://before-interop.github.io/anomalieAdresse/)
- [Documentation métier](https://www.interop-fibre.fr)
