# database.py
# Configure la connexion SQLite et fournit la session de base de données

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Création du moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Nécessaire pour SQLite
)

# Fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles
Base = declarative_base()


def get_db():
    """
    Fournit une session de base de données.
    Utilisé comme dépendance dans les routes FastAPI.
    Se ferme automatiquement après chaque requête.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()