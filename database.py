# database.py
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NetWatchDatabase")

SQLALCHEMY_DATABASE_URL = "sqlite:///./netwatch.db"

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Base de données initialisée avec succès.")
except Exception as e:
    logger.error(f"Erreur critique base de données : {e}")
    raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Erreur de session SQL : {e}")
        db.rollback()
        raise
    finally:
        db.close()