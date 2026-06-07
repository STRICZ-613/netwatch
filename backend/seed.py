# backend/seed.py
import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NetWatchSeed")

# On recrée directement la connexion SQLite de manière autonome ici
SQLALCHEMY_DATABASE_URL = "sqlite:///./netwatch.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def alimenter_base_de_donnees():
    db = SessionLocal()
    try:
        logger.info("Création des tables et injection des données de simulation...")
        models.Base.metadata.create_all(bind=engine)
        # On s'assure que les tables existent bien dans ce fichier de base de données
        
        
        # 1. Ajout d'appareils de test si la table est vide
        if db.query(models.Appareil).count() == 0:
            appareils_test = [
                models.Appareil(mac="00:1A:2B:3C:4D:5E", ip="192.168.1.1", nom="Routeur Principal", categorie="Passerelle", est_connu=True),
                models.Appareil(mac="00:1A:2B:3C:4D:5F", ip="192.168.1.2", nom="Switch Commutateur", categorie="Équipement Réseau", est_connu=True),
                models.Appareil(mac="AA:BB:CC:DD:EE:FF", ip="192.168.1.50", nom="PC Portable Direction", categorie="Ordinateur", est_connu=True),
                models.Appareil(mac="FF:EE:DD:CC:BB:AA", ip="192.168.1.99", nom="Équipement Suspect", categorie="Inconnu", est_connu=False)
            ]
            db.add_all(appareils_test)
            logger.info("Appareils de simulation ajoutés.")
        
        # 2. Ajout d'événements/alertes de test si la table est vide
        if db.query(models.Evenement).count() == 0:
            evenements_test = [
                models.Evenement(mac_appareil="00:1A:2B:3C:4D:5E", type_evenement="CONNEXION", description="Routeur démarré et connecté au réseau."),
                models.Evenement(mac_appareil="FF:EE:DD:CC:BB:AA", type_evenement="INTRUSION", description="Adresse MAC inconnue détectée sur le réseau de l'établissement !")
            ]
            db.add_all(evenements_test)
            logger.info("Événements de simulation ajoutés.")

        # 3. Ajout de ports ouverts de test si la table est vide
        if db.query(models.ScanPort).count() == 0:
            ports_test = [
                models.ScanPort(mac_appareil="00:1A:2B:3C:4D:5E", port=80, protocole="TCP", statut="Ouvert"),
                models.ScanPort(mac_appareil="00:1A:2B:3C:4D:5E", port=443, protocole="TCP", statut="Ouvert"),
                models.ScanPort(mac_appareil="AA:BB:CC:DD:EE:FF", port=22, protocole="TCP", statut="Ouvert")
            ]
            db.add_all(ports_test)
            logger.info("Ports scannés de simulation ajoutés.")

        db.commit()
        logger.info("Base de données initialisée avec succès !")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de l'injection : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    alimenter_base_de_donnees()