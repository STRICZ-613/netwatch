<<<<<<< HEAD
from fastapi import FastAPI
from database import engine, Base
# On importe uniquement les objets 'router' définis dans tes fichiers
from routers.devices import router as devices_router
from routers.logs import router as logs_router
from routers.ports import router as ports_router

app = FastAPI(
    title="NetWatch API",
    description="API robuste pour la surveillance réseau",
    version="1.0.0"
)

# Initialisation de la base de données
Base.metadata.create_all(bind=engine)

# Connexion des routeurs (on utilise les noms aliasés)
app.include_router(devices_router, prefix="/devices", tags=["Devices"])
app.include_router(logs_router, prefix="/logs", tags=["Logs"])
app.include_router(ports_router, prefix="/ports", tags=["Ports"])

@app.get("/")
def read_root():
    return {"message": "API NetWatch opérationnelle"}
=======
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
>>>>>>> cbbb7dbc5814440e679a50ccb0f817373251dd61
