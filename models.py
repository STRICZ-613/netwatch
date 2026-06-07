# models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

# Tableau 1 : Pour stocker les équipements réseau découverts
class Appareil(Base):
    __tablename__ = "appareils"

    id = Column(Integer, primary_key=True, index=True)
    mac = Column(String, unique=True, index=True, nullable=False) # L'adresse MAC unique (obligatoire)
    ip = Column(String, nullable=False)                            # L'adresse IP (obligatoire)
    nom = Column(String, default="Équipement Inconnu")
    categorie = Column(String, default="Non classé")
    est_connu = Column(Boolean, default=True)                      # False si c'est un intrus !
    premiere_connexion = Column(DateTime, default=datetime.utcnow)
    derniere_connexion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Tableau 2 : Pour stocker l'historique des alertes et connexions
class Evenement(Base):
    __tablename__ = "evenements"

    id = Column(Integer, primary_key=True, index=True)
    mac_appareil = Column(String, index=True, nullable=False)
    type_evenement = Column(String, nullable=False) # Ex: "CONNEXION", "INTRUSION", "DECONNEXION"
    description = Column(String)
    horodatage = Column(DateTime, default=datetime.utcnow)

# Tableau 3 : Pour stocker les ports réseaux ouverts trouvés lors des scans
class ScanPort(Base):
    __tablename__ = "scan_ports"

    id = Column(Integer, primary_key=True, index=True)
    mac_appareil = Column(String, index=True, nullable=False)
    port = Column(Integer, nullable=False)
    protocole = Column(String, default="TCP")       # TCP ou UDP
    statut = Column(String, default="Ouvert")        # Ouvert ou Fermé
    scanne_le = Column(DateTime, default=datetime.utcnow)