# routers/stats.py
# Gère les endpoints de statistiques et le WebSocket temps réel

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from database import get_db
from models import ScanPort
from services import simulator
from config import USE_REAL_SCANNER

router = APIRouter()


# ─────────────────────────────────────────────
# GESTIONNAIRE DE CONNEXIONS WEBSOCKET
# Garde en mémoire tous les clients connectés
# monitor.py l'utilise pour envoyer des événements en temps réel
# ─────────────────────────────────────────────
class GestionnaireConnexions:
    def __init__(self):
        self.connexions_actives: list[WebSocket] = []

    async def connecter(self, websocket: WebSocket):
        await websocket.accept()
        self.connexions_actives.append(websocket)

    def deconnecter(self, websocket: WebSocket):
        self.connexions_actives.remove(websocket)

    async def diffuser(self, message: dict):
        """
        Envoie un message à tous les clients connectés.
        Appelé par monitor.py quand un événement est détecté.
        """
        for connexion in self.connexions_actives:
            try:
                await connexion.send_json(message)
            except Exception:
                pass


# Instance globale utilisée par monitor.py
gestionnaire = GestionnaireConnexions()


# ─────────────────────────────────────────────
# SCHÉMAS DE DONNÉES
# ─────────────────────────────────────────────
class PortReponse(BaseModel):
    port: int
    protocole: str
    statut: str
    description: str

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint WebSocket principal.
    Le frontend s'y connecte via useWebSocket.js pour recevoir
    les alertes et mises à jour en temps réel.
    """
    await gestionnaire.connecter(websocket)
    try:
        while True:
            # On attend des messages du client
            # (le client peut envoyer "ping" pour maintenir la connexion)
            await websocket.receive_text()
    except WebSocketDisconnect:
        gestionnaire.deconnecter(websocket)


@router.get("/bandwidth")
def get_bande_passante():
    """
    Retourne la vitesse d'envoi et de réception actuelle.
    Appelé par BandwidthChart.jsx pour les mises à jour en direct.
    """
    if USE_REAL_SCANNER:
        from services.scanner import get_bandwidth_stats
        return get_bandwidth_stats()
    else:
        return simulator.get_simulated_bandwidth()


@router.get("/history")
def get_historique_bande_passante():
    """
    Retourne l'historique de bande passante pour les graphes.
    Appelé au chargement initial de BandwidthChart.jsx.
    """
    return simulator.get_bandwidth_history()


@router.get("/portscan")
def get_scan_ports(mac: str, db: Session = Depends(get_db)):
    """
    Retourne les ports ouverts pour un appareil donné.
    Appelé par PortChecker.jsx quand l'utilisateur lance un scan.
    Les résultats sont simulés mais réalistes selon le type d'appareil.
    """
    resultats = simulator.get_simulated_ports(mac)
    return resultats