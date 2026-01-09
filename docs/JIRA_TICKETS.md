# Tickets Techniques - Workflow Complet Anomalie Adresse

## Epic: AXIONE-EPIC-001

**Titre:** Implémentation du workflow complet de gestion des anomalies d'adresse

**Description:**
Mise en place du système complet de gestion des anomalies d'adresse côté OI (Opérateur d'Infrastructure), incluant le moteur de workflow, l'intégration Kafka et ITSM, ainsi que l'observabilité.

**Workflow cible:**
```
OC → ACKNOWLEDGED → IN_PROGRESS → RESOLVED → CLOSED
                  ↘ PENDING ↗        ↘ REJECTED
                  ↘ CANCELED
```

---

## AXIONE-001: Implémentation du moteur de workflow (State Machine)

**Type:** Story
**Priorité:** High
**Estimation:** 5 points

### Description
Implémenter un moteur de workflow basé sur une machine à états pour gérer les transitions de statut des anomalies conformément à la spécification Interop.

### Critères d'acceptation
- [ ] Les statuts suivants sont implémentés: ACKNOWLEDGED, IN_PROGRESS, PENDING, RESOLVED, CLOSED, REJECTED, CANCELED
- [ ] Les transitions valides sont définies et respectent le workflow Interop:
  - ACKNOWLEDGED → IN_PROGRESS, REJECTED, CANCELED
  - IN_PROGRESS → PENDING, RESOLVED, CANCELED
  - PENDING → IN_PROGRESS (info fournie), RESOLVED (délai dépassé), CANCELED
  - RESOLVED → ACKNOWLEDGED (refus OC), CLOSED
  - CLOSED → (terminal)
  - REJECTED → (terminal)
  - CANCELED → (terminal)
- [ ] Les transitions invalides retournent une erreur 403 Forbidden
- [ ] Le champ `statusChangeReason` est obligatoire pour chaque transition
- [ ] Les motifs suivants sont supportés: INVALID, DUPLICATE, UNKNOWN_RESOURCE, WAITING_INFORMATION, INFORMATION_PROVIDED, RESOLVED, UNRESOLVABLE, REQUALIFIED, RESOLUTION_ACCEPTED, RESOLUTION_REFUSED, DELAY_ANSWER_EXPIRED, DELAY_VALIDATION_EXPIRED
- [ ] Le champ `complexity` (SIMPLE, COMPLEXE, MASSE) est renseigné à la qualification
- [ ] Les durées sont calculées: acknowledgedDuration, totalInProgressDuration, totalPendingDuration, resolvedToClosedDuration
- [ ] Les tests unitaires couvrent toutes les transitions (valides et invalides)

### Dépendances
- Aucune

---

## AXIONE-002: Intégration Kafka - Producer d'événements

**Type:** Story
**Priorité:** High
**Estimation:** 5 points

### Description
Implémenter un producer Kafka pour publier des événements lors des changements de statut afin de notifier les systèmes en aval (ITSM, OC) de manière asynchrone.

### Critères d'acceptation
- [ ] Un producer Kafka est configuré avec les paramètres de connexion externalisés
- [ ] Les événements suivants sont publiés:
  - `fr.interop.anomalieadresse.create` - création d'anomalie
  - `fr.interop.anomalieadresse.update` - mise à jour de statut
  - `fr.interop.anomalieadresse.note.create` - ajout de note
  - `fr.interop.anomalieadresse.attachment.create` - ajout de pièce jointe
- [ ] Les événements suivent un format standardisé (JSON)
- [ ] Un mécanisme de retry est implémenté en cas d'échec de publication
- [ ] Les événements non publiés sont stockés pour retraitement (outbox pattern)
- [ ] Les métriques de publication sont exposées (succès, échecs, latence)

### Dépendances
- AXIONE-001 (State Machine)

---

## AXIONE-003: Intégration Kafka - Consumer ITSM

**Type:** Story
**Priorité:** High
**Estimation:** 5 points

### Description
Implémenter un consumer Kafka pour consommer les événements de l'ITSM et mettre à jour le statut des anomalies automatiquement.

### Critères d'acceptation
- [ ] Un consumer Kafka est configuré pour le topic ITSM
- [ ] Les événements ITSM sont mappés vers les statuts Interop
- [ ] Les mises à jour de statut déclenchent le workflow (state machine)
- [ ] Les événements invalides sont envoyés vers une Dead Letter Queue (DLQ)
- [ ] Un mécanisme d'idempotence est implémenté (éviter les doublons)
- [ ] Les métriques de consommation sont exposées

### Mapping ITSM → Interop
| Statut ITSM | Statut Interop |
|-------------|----------------|
| OPEN | IN_PROGRESS |
| ON_HOLD | PENDING |
| RESOLVED | RESOLVED |
| CLOSED | CLOSED |
| REJECTED | REJECTED |

### Dépendances
- AXIONE-001 (State Machine)
- AXIONE-002 (Kafka Producer)

---

## AXIONE-004: Intégration ITSM

**Type:** Story
**Priorité:** High
**Estimation:** 8 points

### Description
Implémenter l'intégration ITSM pour créer automatiquement un ticket lors de la création d'une anomalie et synchroniser les statuts de manière bidirectionnelle.

### Critères d'acceptation
- [ ] Un client ITSM est implémenté (REST API)
- [ ] La création d'anomalie déclenche la création d'un ticket ITSM
- [ ] L'ID du ticket ITSM est stocké dans l'anomalie
- [ ] Les notes ajoutées à l'anomalie sont synchronisées vers l'ITSM
- [ ] Les pièces jointes sont uploadées vers l'ITSM
- [ ] Un circuit breaker est implémenté pour gérer les pannes ITSM
- [ ] Les appels ITSM sont retryés avec backoff exponentiel

### Dépendances
- AXIONE-001 (State Machine)
- AXIONE-003 (Kafka Consumer)

---

## AXIONE-005: Observabilité (Logging, Metrics)

**Type:** Story
**Priorité:** Medium
**Estimation:** 3 points

### Description
Mettre en place le logging et les métriques pour faciliter le monitoring en production.

### Critères d'acceptation

#### Logging
- [ ] Les logs sont structurés en JSON
- [ ] Chaque requête a un correlation ID unique
- [ ] Les événements métier sont loggés (création, transition, erreur)

#### Métriques
- [ ] Endpoint `/metrics` expose les métriques Prometheus
- [ ] Métriques de base: requêtes HTTP, anomalies créées, transitions

### Dépendances
- Aucune (peut être fait en parallèle)

---

## AXIONE-006: Tests E2E

**Type:** Story
**Priorité:** Medium
**Estimation:** 3 points

### Description
Mettre en place des tests E2E pour valider le workflow complet.

### Critères d'acceptation
- [ ] Tests E2E du workflow complet
- [ ] Couverture des scénarios principaux

### Scénarios E2E à couvrir
1. Happy path: Création → IN_PROGRESS → RESOLVED → CLOSED
2. Annulation: Création → CANCELED
3. Rejet: Création → REJECTED

### Dépendances
- AXIONE-001 à AXIONE-005

---

## AXIONE-007: Endpoints Notes et Pièces jointes

**Type:** Story
**Priorité:** Low
**Estimation:** 5 points

### Description
Implémenter les endpoints pour ajouter des notes et des pièces jointes à une anomalie afin de fournir des informations complémentaires.

### Critères d'acceptation

#### Notes
- [ ] POST `/anomalie-adresse/{id}/note` - Créer une note
- [ ] GET `/anomalie-adresse/{id}/note` - Lister les notes (paginé)
- [ ] HEAD `/anomalie-adresse/{id}/note` - Compter les notes
- [ ] Les notes sont synchronisées vers l'ITSM

#### Pièces jointes
- [ ] POST `/anomalie-adresse/{id}/attachment` - Uploader un fichier
- [ ] GET `/anomalie-adresse/{id}/attachment` - Lister les fichiers (paginé)
- [ ] GET `/anomalie-adresse/{id}/attachment/{attachmentId}/content` - Télécharger
- [ ] Types MIME autorisés: CSV, JPEG, PNG, SVG, PDF, ODT, ODS, DOCX, XLSX
- [ ] Taille maximale: 10 MB
- [ ] Stockage: S3 ou système de fichiers local
- [ ] Les fichiers sont synchronisés vers l'ITSM

### Dépendances
- AXIONE-004 (ITSM Integration)

---
