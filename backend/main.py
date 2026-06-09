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