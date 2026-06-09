# main.py
# Point d'entrée de l'application NetWatch
# Crée l'application FastAPI, enregistre les routeurs et démarre le monitoring

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import Base, engine
from routers import devices, alerts, logs, stats
from services import monitor


# ─────────────────────────────────────────────
# CRÉATION DES TABLES AU DÉMARRAGE
# ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Exécuté au démarrage et à l'arrêt du serveur.
    - Crée les tables de la base de données si elles n'existent pas
    - Démarre la boucle de surveillance réseau en arrière-plan
    """
    # Démarrage
    Base.metadata.create_all(bind=engine)
    monitor.demarrer()
    yield
    # Arrêt
    monitor.arreter()


# ─────────────────────────────────────────────
# INITIALISATION DE L'APPLICATION
# ─────────────────────────────────────────────
app = FastAPI(
    title="NetWatch API",
    description="API du tableau de bord de surveillance réseau NetWatch",
    version="1.0.0",
    lifespan=lifespan
)


# ─────────────────────────────────────────────
# CONFIGURATION CORS
# Permet au frontend React (port 5173) de communiquer avec le backend
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# ENREGISTREMENT DES ROUTEURS
# Chaque routeur gère une section de l'API
# ─────────────────────────────────────────────
app.include_router(devices.router, prefix="/devices", tags=["Appareils"])
app.include_router(alerts.router,  prefix="/alerts",  tags=["Alertes"])
app.include_router(logs.router,    prefix="/logs",    tags=["Journaux"])
app.include_router(stats.router,   prefix="/stats",   tags=["Statistiques"])


# ─────────────────────────────────────────────
# ROUTE DE VÉRIFICATION
# ─────────────────────────────────────────────
@app.get("/")
def racine():
    return {"message": "NetWatch API en ligne", "statut": "ok"}