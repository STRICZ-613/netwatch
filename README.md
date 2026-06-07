# NetWatch — Tableau de bord de surveillance réseau

Application web de surveillance et sécurité réseau en temps réel.

## Prérequis

- Python 3.11+
- Node.js 18+

## Installation

### Backend
cd backend
pip install -r requirements.txt

### Frontend
cd frontend
npm install

## Démarrage

### Backend
cd backend
uvicorn main:app --reload

### Frontend
cd frontend
npm run dev

## Mode démonstration

Dans `backend/config.py`, mettre `USE_REAL_SCANNER = False` pour
utiliser les données simulées (recommandé pour la présentation).