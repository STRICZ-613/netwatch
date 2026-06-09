# services/simulator.py
# Contient toutes les données simulées pour le mode démonstration
# Ce fichier est utilisé quand USE_REAL_SCANNER = False dans config.py

import random
from datetime import datetime, timedelta


# ─────────────────────────────────────────────
# LISTE DES APPAREILS SIMULÉS
# Représente un réseau domestique réaliste
# ─────────────────────────────────────────────
APPAREILS_SIMULES = [
    {
        "mac": "AA:BB:CC:DD:EE:01",
        "ip": "192.168.1.1",
        "nom": "Routeur Principal",
        "categorie": "Réseau",
        "est_connu": True,
        "en_ligne": True,
    },
    {
        "mac": "AA:BB:CC:DD:EE:02",
        "ip": "192.168.1.10",
        "nom": "PC Bureau - Salon",
        "categorie": "Ordinateur",
        "est_connu": True,
        "en_ligne": True,
    },
    {
        "mac": "AA:BB:CC:DD:EE:03",
        "ip": "192.168.1.11",
        "nom": "Laptop - Chambre",
        "categorie": "Ordinateur",
        "est_connu": True,
        "en_ligne": True,
    },
    {
        "mac": "AA:BB:CC:DD:EE:04",
        "ip": "192.168.1.20",
        "nom": "iPhone - Papa",
        "categorie": "Téléphone",
        "est_connu": True,
        "en_ligne": True,
    },
    {
        "mac": "AA:BB:CC:DD:EE:05",
        "ip": "192.168.1.21",
        "nom": "Samsung Galaxy - Maman",
        "categorie": "Téléphone",
        "est_connu": True,
        "en_ligne": False,
    },
    {
        "mac": "AA:BB:CC:DD:EE:06",
        "ip": "192.168.1.30",
        "nom": "Smart TV - Salon",
        "categorie": "Divertissement",
        "est_connu": True,
        "en_ligne": True,
    },
    {
        "mac": "AA:BB:CC:DD:EE:07",
        "ip": "192.168.1.31",
        "nom": "Console PS5",
        "categorie": "Divertissement",
        "est_connu": True,
        "en_ligne": False,
    },
    {
        "mac": "AA:BB:CC:DD:EE:08",
        "ip": "192.168.1.40",
        "nom": "Imprimante HP",
        "categorie": "Périphérique",
        "est_connu": True,
        "en_ligne": True,
    },
    {
        "mac": "AA:BB:CC:DD:EE:09",
        "ip": "192.168.1.50",
        "nom": "Caméra IP - Entrée",
        "categorie": "Sécurité",
        "est_connu": True,
        "en_ligne": True,
    },
    {
        "mac": "AA:BB:CC:DD:EE:10",
        "ip": "192.168.1.51",
        "nom": "Enceinte Connectée",
        "categorie": "Divertissement",
        "est_connu": True,
        "en_ligne": True,
    },
]

# Appareil suspect utilisé pour la démonstration
APPAREIL_DEMO = {
    "mac": "FF:FF:FF:FF:FF:99",
    "ip": "192.168.1.99",
    "nom": "Appareil inconnu",
    "categorie": "Non catégorisé",
    "est_connu": False,
    "en_ligne": True,
}


# ─────────────────────────────────────────────
# PORTS SIMULÉS PAR CATÉGORIE D'APPAREIL
# ─────────────────────────────────────────────
PORTS_PAR_CATEGORIE = {
    "Réseau": [
        {"port": 80,   "protocole": "TCP", "statut": "ouvert",  "description": "HTTP - Interface d'administration"},
        {"port": 443,  "protocole": "TCP", "statut": "ouvert",  "description": "HTTPS - Interface sécurisée"},
        {"port": 53,   "protocole": "UDP", "statut": "ouvert",  "description": "DNS - Résolution de noms"},
        {"port": 22,   "protocole": "TCP", "statut": "suspect", "description": "SSH - Accès distant (vérifier si nécessaire)"},
    ],
    "Ordinateur": [
        {"port": 135,  "protocole": "TCP", "statut": "ouvert",  "description": "RPC - Appel de procédures distantes"},
        {"port": 445,  "protocole": "TCP", "statut": "ouvert",  "description": "SMB - Partage de fichiers Windows"},
        {"port": 3389, "protocole": "TCP", "statut": "suspect", "description": "RDP - Bureau à distance (risque si exposé)"},
    ],
    "Téléphone": [
        {"port": 5353, "protocole": "UDP", "statut": "ouvert",  "description": "mDNS - Découverte de services locaux"},
        {"port": 8080, "protocole": "TCP", "statut": "ouvert",  "description": "HTTP alternatif"},
    ],
    "Divertissement": [
        {"port": 1900, "protocole": "UDP", "statut": "ouvert",  "description": "SSDP - Découverte UPnP"},
        {"port": 8008, "protocole": "TCP", "statut": "ouvert",  "description": "Chromecast / Cast API"},
    ],
    "Périphérique": [
        {"port": 9100, "protocole": "TCP", "statut": "ouvert",  "description": "RAW Print - Impression directe"},
        {"port": 631,  "protocole": "TCP", "statut": "ouvert",  "description": "IPP - Protocole d'impression Internet"},
    ],
    "Sécurité": [
        {"port": 554,  "protocole": "TCP", "statut": "ouvert",  "description": "RTSP - Flux vidéo en temps réel"},
        {"port": 8000, "protocole": "TCP", "statut": "ouvert",  "description": "HTTP - Interface de gestion caméra"},
    ],
    "Non catégorisé": [
        {"port": 4444,  "protocole": "TCP", "statut": "suspect", "description": "Port suspect - Possible backdoor"},
        {"port": 6666,  "protocole": "TCP", "statut": "suspect", "description": "Port suspect - Activité inhabituelle"},
        {"port": 31337, "protocole": "TCP", "statut": "suspect", "description": "Port suspect - Connu pour malwares"},
    ],
}


# ─────────────────────────────────────────────
# FONCTIONS PUBLIQUES
# ─────────────────────────────────────────────
def get_simulated_devices() -> list[dict]:
    """
    Retourne la liste des appareils simulés.
    Appelé par monitor.py quand USE_REAL_SCANNER = False.
    """
    return APPAREILS_SIMULES


def get_appareil_demo() -> dict:
    """
    Retourne l'appareil suspect pour la démonstration.
    Appelé par monitor.py quand le bouton démo est pressé.
    """
    return APPAREIL_DEMO


def get_simulated_bandwidth() -> dict:
    """
    Retourne des valeurs de bande passante qui fluctuent aléatoirement.
    Simule un réseau domestique actif.
    Appelé par stats.py -> /stats/bandwidth.
    """
    return {
        "envoi_mbps":    round(random.uniform(0.5, 8.0), 2),
        "reception_mbps": round(random.uniform(1.0, 25.0), 2),
        "horodatage":    datetime.now().isoformat()
    }


def get_bandwidth_history() -> list[dict]:
    """
    Génère un historique de bande passante des 30 dernières minutes.
    Utilisé pour afficher les données initiales dans BandwidthChart.jsx.
    """
    historique = []
    maintenant = datetime.now()
    for i in range(30):
        moment = maintenant - timedelta(minutes=30 - i)
        historique.append({
            "envoi_mbps":     round(random.uniform(0.5, 8.0), 2),
            "reception_mbps": round(random.uniform(1.0, 25.0), 2),
            "horodatage":     moment.isoformat()
        })
    return historique


def get_simulated_ports(mac: str) -> list[dict]:
    """
    Retourne les ports ouverts simulés pour un appareil donné.
    Détermine la catégorie de l'appareil par son MAC et retourne
    les ports correspondants.
    Appelé par stats.py -> /stats/portscan.
    """
    # Trouver la catégorie de l'appareil dans la liste simulée
    categorie = "Non catégorisé"
    for appareil in APPAREILS_SIMULES:
        if appareil["mac"] == mac:
            categorie = appareil["categorie"]
            break

    # Retourner les ports correspondants à la catégorie
    return PORTS_PAR_CATEGORIE.get(categorie, PORTS_PAR_CATEGORIE["Non catégorisé"])