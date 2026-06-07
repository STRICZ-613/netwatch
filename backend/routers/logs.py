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