# routers/logs.py
# Gère les endpoints pour le journal d'événements

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database import get_db
from models import Evenement

router = APIRouter()


# ─────────────────────────────────────────────
# SCHÉMAS DE DONNÉES
# ─────────────────────────────────────────────
class EvenementReponse(BaseModel):
    id: int
    mac_appareil: str
    type_evenement: str
    description: str
    horodatage: Optional[datetime]

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────
@router.get("/", response_model=list[EvenementReponse])
def get_journaux(
    type_evenement: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retourne tous les événements du journal.
    Filtrable par type d'événement via paramètre URL.
    Exemple : /logs?type_evenement=connexion
    Utilisé par Logs.jsx pour afficher l'historique complet.
    """
    requete = db.query(Evenement).order_by(Evenement.horodatage.desc())
    if type_evenement:
        requete = requete.filter(Evenement.type_evenement == type_evenement)
    return requete.limit(100).all()


@router.get("/{mac}", response_model=list[EvenementReponse])
def get_journaux_appareil(mac: str, db: Session = Depends(get_db)):
    """
    Retourne tous les événements liés à un appareil spécifique.
    Utilisé par DeviceCard.jsx pour afficher l'historique d'un appareil.
    """
    return (
        db.query(Evenement)
        .filter(Evenement.mac_appareil == mac)
        .order_by(Evenement.horodatage.desc())
        .all()
    )