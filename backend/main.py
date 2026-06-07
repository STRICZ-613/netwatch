# backend/main.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import devices, logs

# 1. Configuration des logs pour suivre la vie de notre API
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NetWatchMain")

# 2. Création automatique des tables dans SQLite si elles n'existent pas encore
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Toutes les tables de la base de données ont été créées ou vérifiées.")
except Exception as e:
    logger.critical(f"Impossible de générer les tables de la base de données : {e}")

# 3. Initialisation de l'application FastAPI
app = FastAPI(
    title="NetWatch API",
    description="Backend robuste pour la surveillance et la détection d'intrusions réseau",
    version="1.0.0"
)

# 4. Configuration du CORS (Sécurité pour permettre au Frontend de parler au Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En développement, on autorise tout le monde pour éviter les blocages
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Inclusion de tes deux super routeurs
app.include_router(devices.router)
app.include_router(logs.router)

# 6. Petite route d'accueil pour tester rapidement si l'API est vivante
@app.get("/", tags=["Racine"])
def route_accueil():
    return {
        "statut": "En ligne",
        "application": "NetWatch API Backend",
        "message": "Bienvenue sur l'API sécurisée. Accédez à /docs pour la documentation."
    }