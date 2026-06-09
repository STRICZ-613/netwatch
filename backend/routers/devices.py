<<<<<<< HEAD
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_ports():
    return {"message": "Liste des ports"}
=======
# routers/devices.py
# Gère tous les endpoints liés aux appareils réseau

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database import get_db
from models import Appareil, Evenement
from services import monitor

router = APIRouter()


# ─────────────────────────────────────────────
# SCHÉMAS DE DONNÉES (Pydantic)
# Définissent le format des données entrantes et sortantes
# ─────────────────────────────────────────────
class AppareilReponse(BaseModel):
    id: int
    mac: str
    ip: str
    nom: str
    categorie: str
    est_connu: bool
    en_ligne: bool
    premiere_connexion: Optional[datetime]
    derniere_connexion: Optional[datetime]

    class Config:
        from_attributes = True


class MiseAJourAppareil(BaseModel):
    nom: Optional[str] = None
    categorie: Optional[str] = None
    est_connu: Optional[bool] = None


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────
@router.get("/", response_model=list[AppareilReponse])
def get_appareils(db: Session = Depends(get_db)):
    """
    Retourne la liste de tous les appareils connus.
    Utilisé par DeviceList.jsx pour afficher le tableau des appareils.
    """
    return db.query(Appareil).all()


@router.get("/{mac}", response_model=AppareilReponse)
def get_appareil(mac: str, db: Session = Depends(get_db)):
    """
    Retourne un seul appareil par son adresse MAC.
    Utilisé par DeviceCard.jsx pour afficher les détails.
    """
    appareil = db.query(Appareil).filter(Appareil.mac == mac).first()
    if not appareil:
        raise HTTPException(status_code=404, detail="Appareil non trouvé")
    return appareil


@router.put("/{mac}", response_model=AppareilReponse)
def modifier_appareil(mac: str, data: MiseAJourAppareil, db: Session = Depends(get_db)):
    """
    Met à jour le nom ou la catégorie d'un appareil.
    Utilisé par DeviceCard.jsx quand l'utilisateur renomme un appareil.
    """
    appareil = db.query(Appareil).filter(Appareil.mac == mac).first()
    if not appareil:
        raise HTTPException(status_code=404, detail="Appareil non trouvé")

    if data.nom is not None:
        appareil.nom = data.nom
    if data.categorie is not None:
        appareil.categorie = data.categorie
    if data.est_connu is not None:
        appareil.est_connu = data.est_connu

    db.commit()
    db.refresh(appareil)
    return appareil


@router.post("/trigger")
async def declencher_demo(db: Session = Depends(get_db)):
    """
    Simule l'apparition d'un appareil inconnu sur le réseau.
    Utilisé par le bouton de démonstration dans Dashboard.jsx.
    Déclenche une alerte en temps réel via WebSocket.
    """
    await monitor.injecter_appareil_demo(db)
    return {"message": "Appareil suspect simulé avec succès"}
>>>>>>> cbbb7dbc5814440e679a50ccb0f817373251dd61
