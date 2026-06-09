from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas 

router = APIRouter(tags=["Scan de Ports"])

@router.post("/{mac}")
def enregistrer_port_ouvert(port_in: schemas.ScanPortCreate, db: Session = Depends(get_db)):
    port_existe = db.query(models.ScanPort).filter(
        models.ScanPort.mac_appareil == port_in.mac_appareil,
        models.ScanPort.port == port_in.port
    ).first()

    if port_existe:
        port_existe.statut = port_in.statut
        db.commit()
        return {"message": "Statut du port mis à jour", "data": port_existe}

    nouveau_port = models.ScanPort(**port_in.dict())
    db.add(nouveau_port)
    db.commit()
    db.refresh(nouveau_port)
    return {"message": "Port ouvert enregistré", "data": nouveau_port}

@router.get("/{mac}")
def lister_ports_appareil(mac: str, db: Session = Depends(get_db)):
    return db.query(models.ScanPort).filter(models.ScanPort.mac_appareil == mac).all()