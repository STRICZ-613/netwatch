from pydantic import BaseModel

# Structure pour valider les données reçues depuis l'extérieur
class DeviceCreate(BaseModel):
    mac: str
    ip: str
    nom: str = "Équipement Inconnu"
    categorie: str = "Non classé"

@router.post("", status_code=status.HTTP_201_CREATED)
def enregistrer_appareil(device_in: DeviceCreate, db: Session = Depends(get_db)):
    """Enregistre ou met à jour un appareil détecté sur le réseau"""
    try:
        # On vérifie si l'appareil existe déjà avec cette adresse MAC
        appareil_existe = db.query(models.Appareil).filter(models.Appareil.mac == device_in.mac).first()
        
        if appareil_existe:
            # S'il existe, on met juste à jour son IP et sa date de dernière connexion
            appareil_existe.ip = device_in.ip
            db.commit()
            return {"message": "Appareil déjà existant, IP mise à jour", "data": appareil_existe}
        
        # S'il est nouveau, on le crée
        nouvel_appareil = models.Appareil(
            mac=device_in.mac,
            ip=device_in.ip,
            nom=device_in.nom,
            categorie=device_in.categorie
        )
        db.add(nouvel_appareil)
        db.commit()
        db.refresh(nouvel_appareil)
        return {"message": "Nouvel appareil enregistré avec succès", "data": nouvel_appareil}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'enregistrement de l'appareil : {str(e)}"
        )