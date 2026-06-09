# services/monitor.py
# Boucle de surveillance réseau en arrière-plan
# Tourne en continu pendant que le serveur est actif
# Détecte les nouveaux appareils et pousse les alertes via WebSocket

import asyncio
from datetime import datetime
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Appareil, Evenement
from config import USE_REAL_SCANNER, NETWORK_RANGE, SCAN_INTERVAL
from services import simulator

# Importation du gestionnaire WebSocket depuis stats.py
# Ce gestionnaire contient la liste de tous les clients connectés
from routers.stats import gestionnaire

# ─────────────────────────────────────────────
# ÉTAT INTERNE DU MONITEUR
# ─────────────────────────────────────────────
_tache_monitoring = None        # Référence à la tâche asyncio en cours
_en_cours         = False       # True si la boucle est active


# ─────────────────────────────────────────────
# FONCTIONS DE CONTRÔLE
# Appelées par main.py au démarrage et à l'arrêt
# ─────────────────────────────────────────────
def demarrer():
    """
    Démarre la boucle de surveillance en arrière-plan.
    Appelé par main.py au démarrage du serveur.
    """
    global _tache_monitoring, _en_cours
    _en_cours = True
    loop = asyncio.get_event_loop()
    _tache_monitoring = loop.create_task(_boucle_monitoring())
    print("[Monitor] Surveillance réseau démarrée")


def arreter():
    """
    Arrête proprement la boucle de surveillance.
    Appelé par main.py à l'arrêt du serveur.
    """
    global _en_cours
    _en_cours = False
    if _tache_monitoring:
        _tache_monitoring.cancel()
    print("[Monitor] Surveillance réseau arrêtée")


# ─────────────────────────────────────────────
# BOUCLE PRINCIPALE
# ─────────────────────────────────────────────
async def _boucle_monitoring():
    """
    Boucle infinie qui scanne le réseau toutes les SCAN_INTERVAL secondes.
    Pour chaque scan :
      1. Récupère la liste des appareils (réels ou simulés)
      2. Compare avec la base de données
      3. Enregistre les nouveaux appareils
      4. Détecte les appareils inconnus
      5. Pousse les alertes via WebSocket
    """
    # Initialisation de la base de données avec les appareils simulés
    await _initialiser_appareils_simules()

    while _en_cours:
        try:
            await _executer_scan()
        except Exception as e:
            print(f"[Monitor] Erreur dans la boucle : {e}")

        await asyncio.sleep(SCAN_INTERVAL)


async def _initialiser_appareils_simules():
    """
    Au premier démarrage en mode simulé, peuple la base de données
    avec les appareils de simulator.py si elle est vide.
    """
    if USE_REAL_SCANNER:
        return

    db = SessionLocal()
    try:
        nombre = db.query(Appareil).count()
        if nombre == 0:
            print("[Monitor] Initialisation des appareils simulés...")
            for donnees in simulator.get_simulated_devices():
                appareil = Appareil(
                    mac               = donnees["mac"],
                    ip                = donnees["ip"],
                    nom               = donnees["nom"],
                    categorie         = donnees["categorie"],
                    est_connu         = donnees["est_connu"],
                    en_ligne          = donnees["en_ligne"],
                    premiere_connexion = datetime.now(),
                    derniere_connexion = datetime.now(),
                )
                db.add(appareil)

                # Enregistrement de l'événement de connexion initial
                evenement = Evenement(
                    mac_appareil   = donnees["mac"],
                    type_evenement = "connexion",
                    description    = f"{donnees['nom']} connecté au réseau",
                    horodatage     = datetime.now(),
                )
                db.add(evenement)

            db.commit()
            print(f"[Monitor] {len(simulator.get_simulated_devices())} appareils initialisés")
    finally:
        db.close()


async def _executer_scan():
    """
    Exécute un cycle de scan complet.
    Récupère les appareils actifs et met à jour la base de données.
    """
    db = SessionLocal()
    try:
        if USE_REAL_SCANNER:
            from services.scanner import arp_scan
            appareils_detectes = arp_scan(NETWORK_RANGE)
        else:
            appareils_detectes = simulator.get_simulated_devices()

        macs_detectes = {a["mac"] for a in appareils_detectes}

        # Marquer les appareils non détectés comme hors ligne
        tous_appareils = db.query(Appareil).all()
        for appareil in tous_appareils:
            if appareil.mac not in macs_detectes and appareil.en_ligne:
                appareil.en_ligne = False
                _enregistrer_evenement(db, appareil.mac, "deconnexion",
                    f"{appareil.nom} déconnecté du réseau")

        # Traitement de chaque appareil détecté
        for donnees in appareils_detectes:
            await _traiter_appareil(db, donnees)

        db.commit()

    finally:
        db.close()


async def _traiter_appareil(db: Session, donnees: dict):
    """
    Traite un appareil détecté pendant le scan.
    Crée ou met à jour l'entrée en base de données.
    Déclenche une alerte si l'appareil est inconnu.
    """
    existant = db.query(Appareil).filter(
        Appareil.mac == donnees["mac"]
    ).first()

    if existant is None:
        # Nouvel appareil — on le crée
        nouvel_appareil = Appareil(
            mac                = donnees["mac"],
            ip                 = donnees["ip"],
            nom                = donnees.get("nom", "Appareil inconnu"),
            categorie          = donnees.get("categorie", "Non catégorisé"),
            est_connu          = donnees.get("est_connu", False),
            en_ligne           = True,
            premiere_connexion = datetime.now(),
            derniere_connexion = datetime.now(),
        )
        db.add(nouvel_appareil)
        db.flush()

        # Événement de connexion
        _enregistrer_evenement(db, donnees["mac"], "connexion",
            f"Nouvel appareil détecté : {donnees.get('nom', 'Inconnu')}")

        # Alerte si inconnu
        if not donnees.get("est_connu", False):
            await _alerter_appareil_inconnu(db, donnees)

    else:
        # Appareil connu — mise à jour
        if not existant.en_ligne:
            # Il était hors ligne, il vient de se reconnecter
            _enregistrer_evenement(db, existant.mac, "connexion",
                f"{existant.nom} reconnecté au réseau")

        existant.ip                = donnees["ip"]
        existant.en_ligne          = True
        existant.derniere_connexion = datetime.now()


async def _alerter_appareil_inconnu(db: Session, donnees: dict):
    """
    Enregistre une alerte de sécurité et la pousse via WebSocket
    pour tous les clients frontend connectés.
    """
    _enregistrer_evenement(
        db,
        donnees["mac"],
        "inconnu_detecte",
        f"Appareil non autorisé détecté : IP {donnees['ip']} — MAC {donnees['mac']}"
    )

    # Message WebSocket envoyé au frontend en temps réel
    await gestionnaire.diffuser({
        "type":        "alerte",
        "sous_type":   "inconnu_detecte",
        "mac":         donnees["mac"],
        "ip":          donnees["ip"],
        "nom":         donnees.get("nom", "Appareil inconnu"),
        "message":     f"Appareil inconnu détecté : {donnees['ip']}",
        "horodatage":  datetime.now().isoformat()
    })


def _enregistrer_evenement(db: Session, mac: str, type_evt: str, description: str):
    """
    Crée un enregistrement d'événement dans la base de données.
    Fonction utilitaire utilisée dans tout ce fichier.
    """
    evenement = Evenement(
        mac_appareil   = mac,
        type_evenement = type_evt,
        description    = description,
        horodatage     = datetime.now(),
    )
    db.add(evenement)


# ─────────────────────────────────────────────
# BOUTON DÉMONSTRATION
# ─────────────────────────────────────────────
async def injecter_appareil_demo(db: Session):
    """
    Simule l'apparition d'un appareil suspect sur le réseau.
    Appelé par devices.py -> POST /devices/trigger.
    Déclenche une alerte visible en temps réel dans le frontend.
    """
    donnees = simulator.get_appareil_demo()

    # Vérifier si l'appareil demo existe déjà, le supprimer pour
    # pouvoir le réinjecter à chaque appui sur le bouton
    existant = db.query(Appareil).filter(
        Appareil.mac == donnees["mac"]
    ).first()
    if existant:
        db.delete(existant)
        db.commit()

    # Créer l'appareil suspect
    appareil_demo = Appareil(
        mac                = donnees["mac"],
        ip                 = donnees["ip"],
        nom                = donnees["nom"],
        categorie          = donnees["categorie"],
        est_connu          = False,
        en_ligne           = True,
        premiere_connexion = datetime.now(),
        derniere_connexion = datetime.now(),
    )
    db.add(appareil_demo)

    # Enregistrer l'événement
    _enregistrer_evenement(
        db,
        donnees["mac"],
        "demo",
        f"[DÉMO] Appareil suspect simulé : IP {donnees['ip']}"
    )
    db.commit()

    # Pousser l'alerte via WebSocket
    await gestionnaire.diffuser({
        "type":       "alerte",
        "sous_type":  "demo",
        "mac":        donnees["mac"],
        "ip":         donnees["ip"],
        "nom":        donnees["nom"],
        "message":    "⚠️ Appareil suspect détecté sur le réseau !",
        "horodatage": datetime.now().isoformat()
    })

    print(f"[Monitor] Appareil démo injecté : {donnees['ip']}")