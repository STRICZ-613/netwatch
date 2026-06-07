# backend/routers/devices.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db  # Les deux petits points signifient "revenir en arrière dans le dossier backend"
from .. import models

router = APIRouter(prefix="/api/devices", tags=["Appareils"])

@router.get("")
def liste_appareils(db: Session = Depends(get_db)):
    """Récupère la liste de tous les appareils de manière sécurisée"""
    try:
        appareils = db.query(models.Appareil).all()
        return appareils
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Impossible de récupérer les appareils : {str(e)}"
        )