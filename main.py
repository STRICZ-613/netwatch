from fastapi import FastAPI
from database import engine, Base
import devices, logs, ports  # 1. On importe tes trois modules

# 2. Création automatique des tables
Base.metadata.create_all(bind=engine)

# 3. Initialisation de l'application
app = FastAPI(
    title="NetWatch API",
    description="Backend robuste pour la surveillance réseau",
    version="1.0.0"
)

# 4. Connexion des routes (C'est ici que le "cerveau" lie les fichiers)
app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(logs.router, prefix="/logs", tags=["logs"])
app.include_router(ports.router, prefix="/ports", tags=["ports"])

# Optionnel : Une petite route de test pour vérifier que le serveur répond
@app.get("/")
def read_root():
    return {"message": "NetWatch Backend est opérationnel !"}