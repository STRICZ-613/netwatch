# models.py
# Définit les tables de la base de données sous forme de classes Python

from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.sql import func
from database import Base


class Appareil(Base):
    """
    Table des appareils découverts sur le réseau.
    Chaque appareil est identifié de manière unique par son adresse MAC.
    """
    __tablename__ = "appareils"

    id          = Column(Integer, primary_key=True, index=True)
    mac         = Column(String, unique=True, index=True, nullable=False)
    ip          = Column(String, nullable=False)
    nom         = Column(String, default="Appareil inconnu")
    categorie   = Column(String, default="Non catégorisé")
    est_connu   = Column(Boolean, default=False)
    en_ligne    = Column(Boolean, default=True)
    premiere_connexion = Column(DateTime, default=func.now())
    derniere_connexion = Column(DateTime, default=func.now())


class Evenement(Base):
    """
    Table des événements réseau.
    Enregistre chaque connexion, déconnexion, ou alerte de sécurité.
    """
    __tablename__ = "evenements"

    id              = Column(Integer, primary_key=True, index=True)
    mac_appareil    = Column(String, index=True, nullable=False)
    type_evenement  = Column(String, nullable=False)
    # Types possibles :
    # "connexion"          - appareil connecté au réseau
    # "deconnexion"        - appareil déconnecté du réseau
    # "inconnu_detecte"    - appareil non autorisé détecté
    # "port_suspect"       - port suspect trouvé
    # "demo"               - événement déclenché manuellement
    description     = Column(String, default="")
    horodatage      = Column(DateTime, default=func.now())


class ScanPort(Base):
    """
    Table des résultats de scan de ports.
    Stocke les ports ouverts trouvés sur chaque appareil.
    """
    __tablename__ = "scan_ports"

    id           = Column(Integer, primary_key=True, index=True)
    mac_appareil = Column(String, index=True, nullable=False)
    port         = Column(Integer, nullable=False)
    protocole    = Column(String, default="TCP")
    statut       = Column(String, default="ouvert")
    # "ouvert"   - port normal
    # "suspect"  - port potentiellement dangereux
    scanne_le    = Column(DateTime, default=func.now())