# backend/routers/logs.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(prefix="/api/logs", tags=["Journaux"])

@router.get("")
def liste_journaux(db: Session = Depends(get_db)):
    """Récupère l'historique des événements du plus récent au plus ancien"""
    try:
        journaux = db.query(models.Evenement).order_by(models.Evenement.horodatage.desc()).all()
        return journaux
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la lecture des journaux : {str(e)}"
        )
from pydantic import BaseModel

class LogCreate(BaseModel):
    mac_appareil: str
    type_evenement: str
    description: str

@router.post("", status_code=status.HTTP_201_CREATED)
def creer_log(log_in: LogCreate, db: Session = Depends(get_db)):
    """Crée manuellement un événement ou une alerte dans l'historique"""
    try:
        nouvel_evenement = models.Evenement(
            mac_appareil=log_in.mac_appareil,
            type_evenement=log_in.type_evenement,
            description=log_in.description
        )
        db.add(nouvel_evenement)
        db.commit()
        db.refresh(nouvel_evenement)
        return nouvel_evenement
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Impossible de créer le log : {str(e)}"
        )

@router.delete("/clear")
def vider_journaux(db: Session = Depends(get_db)):
    """Vide proprement tout l'historique des événements"""
    try:
        db.query(models.Evenement).delete()
        db.commit()
        return {"message": "Tous les journaux d'événements ont été effacés."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression des logs : {str(e)}"
        )