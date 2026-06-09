# services/scanner.py
# Contient la logique de scan réseau réel
# Utilisé uniquement quand USE_REAL_SCANNER = True dans config.py

import psutil
from datetime import datetime

# scapy est importé uniquement si nécessaire pour éviter les erreurs
# si la bibliothèque n'est pas installée en mode démonstration
try:
    from scapy.all import ARP, Ether, srp
    SCAPY_DISPONIBLE = True
except ImportError:
    SCAPY_DISPONIBLE = False


# ─────────────────────────────────────────────
# SCAN DES APPAREILS
# ─────────────────────────────────────────────
def arp_scan(plage_reseau: str) -> list[dict]:
    """
    Envoie des requêtes ARP sur la plage réseau donnée.
    Retourne la liste des appareils qui ont répondu.
    Chaque appareil est un dictionnaire avec mac et ip.

    Exemple de retour :
    [
        {"mac": "AA:BB:CC:DD:EE:01", "ip": "192.168.1.1"},
        {"mac": "AA:BB:CC:DD:EE:02", "ip": "192.168.1.10"},
    ]
    """
    if not SCAPY_DISPONIBLE:
        print("[Scanner] scapy non disponible, retour liste vide")
        return []

    try:
        # Création du paquet ARP broadcast
        paquet_arp = ARP(pdst=plage_reseau)
        paquet_ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        paquet = paquet_ether / paquet_arp

        # Envoi du paquet et récupération des réponses
        # timeout=2 : attend 2 secondes maximum
        # verbose=0 : pas d'affichage dans le terminal
        resultats = srp(paquet, timeout=2, verbose=0)[0]

        appareils = []
        for envoye, recu in resultats:
            appareils.append({
                "mac": recu.hwsrc,
                "ip":  recu.psrc,
            })

        return appareils

    except Exception as e:
        print(f"[Scanner] Erreur lors du scan ARP : {e}")
        return []


# ─────────────────────────────────────────────
# STATISTIQUES DE BANDE PASSANTE
# ─────────────────────────────────────────────

# Stocke les valeurs précédentes pour calculer la différence
_stats_precedentes = None
_horodatage_precedent = None


def get_bandwidth_stats() -> dict:
    """
    Lit les statistiques réseau réelles depuis l'OS via psutil.
    Calcule la vitesse d'envoi et de réception en Mbps
    en comparant avec la mesure précédente.

    Retourne :
    {
        "envoi_mbps"    : float,
        "reception_mbps": float,
        "horodatage"    : str
    }
    """
    global _stats_precedentes, _horodatage_precedent

    stats_actuelles   = psutil.net_io_counters()
    horodatage_actuel = datetime.now()

    # Première mesure — pas encore de différence à calculer
    if _stats_precedentes is None:
        _stats_precedentes    = stats_actuelles
        _horodatage_precedent = horodatage_actuel
        return {
            "envoi_mbps":     0.0,
            "reception_mbps": 0.0,
            "horodatage":     horodatage_actuel.isoformat()
        }

    # Calcul de l'intervalle de temps en secondes
    intervalle = (horodatage_actuel - _horodatage_precedent).total_seconds()
    if intervalle == 0:
        intervalle = 1

    # Calcul des vitesses en Mbps
    # (octets envoyés / intervalle) * 8 bits / 1 000 000 = Mbps
    octets_envoyes  = stats_actuelles.bytes_sent - _stats_precedentes.bytes_sent
    octets_recus    = stats_actuelles.bytes_recv - _stats_precedentes.bytes_recv

    envoi_mbps      = round((octets_envoyes  / intervalle * 8) / 1_000_000, 2)
    reception_mbps  = round((octets_recus    / intervalle * 8) / 1_000_000, 2)

    # Mise à jour des valeurs précédentes
    _stats_precedentes    = stats_actuelles
    _horodatage_precedent = horodatage_actuel

    return {
        "envoi_mbps":     max(0.0, envoi_mbps),
        "reception_mbps": max(0.0, reception_mbps),
        "horodatage":     horodatage_actuel.isoformat()
    }