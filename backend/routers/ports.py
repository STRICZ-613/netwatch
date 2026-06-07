# backend/routers/ports.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from list import List
from pydantic import BaseModel
from ..database import get_db
from .. import models

router = APIRouter(prefix="/api/ports", tags=["Scan de Ports"])

class PortCreate(BaseModel):
    mac_appareil: str
    port: int
    protocole: str = "TCP"
    statut: str = "Ouvert"

@router.post("", status_code=status.HTTP_201_CREATED)
def enregistrer_port_ouvert(port_in: PortCreate, db: Session = Depends(get_db)):
    """Enregistre un port ouvert trouvé lors d'un scan réseau"""
    try:
        # On vérifie si ce port est déjà enregistré pour cet appareil précis
        port_existe = db.query(models.ScanPort).filter(
            models.ScanPort.mac_appareil == port_in.mac_appareil,
            models.ScanPort.port == port_in.port
        ).first()

        if port_existe:
            port_existe.statut = port_in.statut
            db.commit()
            return {"message": "Statut du port mis à jour", "data": port_existe}

        nouveau_port = models.ScanPort(
            mac_appareil=port_in.mac_appareil,
            port=port_in.port,
            protocole=port_in.protocole,
            statut=port_in.statut
        )
        db.add(nouveau_port)
        db.commit()
        db.refresh(nouveau_port)
        return {"message": "Port ouvert enregistré", "data": nouveau_port}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'enregistrement du port : {str(e)}"
        )

@router.get("/{mac}")
def lister_ports_appareil(mac: str, db: Session = Depends(get_db)):
    """Récupère tous les ports ouverts trouvés pour une adresse MAC spécifique"""
    try:
        ports = db.query(models.ScanPort).filter(models.ScanPort.mac_appareil == mac).all()
        return ports
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Impossible de récupérer les ports pour cet appareil : {str(e)}"
        )