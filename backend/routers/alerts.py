# routers/alerts.py
# Gère les endpoints pour les alertes et notifications

from fastapi import APIRouter, Depends
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
class AlerteReponse(BaseModel):
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
@router.get("/", response_model=list[AlerteReponse])
def get_alertes(db: Session = Depends(get_db)):
    """
    Retourne les 20 alertes les plus récentes.
    Utilisé par AlertPanel.jsx pour afficher les notifications.
    Filtre uniquement les événements de type sécurité.
    """
    types_alertes = ["inconnu_detecte", "port_suspect", "demo"]
    return (
        db.query(Evenement)
        .filter(Evenement.type_evenement.in_(types_alertes))
        .order_by(Evenement.horodatage.desc())
        .limit(20)
        .all()
    )


@router.post("/dismiss/{id}")
def ignorer_alerte(id: int, db: Session = Depends(get_db)):
    """
    Supprime une alerte de la base de données.
    Utilisé par le bouton 'Ignorer' dans AlertPanel.jsx.
    """
    alerte = db.query(Evenement).filter(Evenement.id == id).first()
    if alerte:
        db.delete(alerte)
        db.commit()
    return {"message": "Alerte supprimée"}