# config.py
# Fichier de configuration central de NetWatch
# Modifier USE_REAL_SCANNER pour basculer entre mode réel et mode démonstration

import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# MODE DE FONCTIONNEMENT
# True  = scan ARP réel sur le réseau local
# False = données entièrement simulées (pour la présentation)
# ─────────────────────────────────────────────
USE_REAL_SCANNER = False

# ─────────────────────────────────────────────
# PARAMÈTRES RÉSEAU
# ─────────────────────────────────────────────
NETWORK_RANGE = "192.168.1.0/24"   # Plage réseau à scanner
SCAN_INTERVAL = 10                  # Intervalle de scan en secondes

# ─────────────────────────────────────────────
# PARAMÈTRES BASE DE DONNÉES
# ─────────────────────────────────────────────
DATABASE_URL = "sqlite:///./netwatch.db"

# ─────────────────────────────────────────────
# PARAMÈTRES SERVEUR
# ─────────────────────────────────────────────
HOST = "0.0.0.0"
PORT = 8000