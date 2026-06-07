# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Appareil(Base):
    __tablename__ = "appareils"

    id = Column(Integer, primary_key=True, index=True)
    mac = Column(String, unique=True, index=True, nullable=False)
    ip = Column(String, nullable=False)
    nom = Column(String, default="Équipement Inconnu")
    categorie = Column(String, default="Non classé")
    est_connu = Column(Boolean, default=True)
    derniere_connexion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Evenement(Base):
    __tablename__ = "evenements"

    id = Column(Integer, primary_key=True, index=True)
    mac_appareil = Column(String, index=True, nullable=False)
    type_evenement = Column(String, nullable=False)  # ex: INTRUSION, CONNEXION
    description = Column(String, nullable=False)
    horodatage = Column(DateTime, default=datetime.utcnow)

class ScanPort(Base):
    __tablename__ = "scan_ports"

    id = Column(Integer, primary_key=True, index=True)
    mac_appareil = Column(String, index=True, nullable=False)
    port = Column(Integer, nullable=False)
    protocole = Column(String, default="TCP")  # TCP ou UDP
    statut = Column(String, default="Ouvert")   # Ouvert / Fermé
    derniere_verification = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)