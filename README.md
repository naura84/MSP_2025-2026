# MSP 2025-2026 - Outil d’audit et de scan réseau

Ce projet est une application web de sécurité qui permet de lancer des scans réseau, d’analyser les résultats, d’afficher l’historique des audits et de générer des rapports PDF. L’architecture est basée sur un backend FastAPI et une interface HTML/JavaScript.

## Fonctionnalités principales

- Authentification via JWT avec identifiants par défaut (`admin` / `admin123`)
- Scan de hôte via l’API `/scan`
- Scan avancé via Nmap avec support des types `ip` et `url`
- Suivi des scans en tâche de fond via `/nmap_scan` et `/nmap_scan/{job_id}`
- Historique des résultats stockés dans une base SQLite
- Statistiques globales sur les scans
- Génération de rapports PDF
- Suppression d’un scan spécifique
- Vérification de l’état de la base de données et du service

## Structure du projet

```text
MSP_2025-2026/
├── backend/
│   ├── auth/
│   │   └── auth_handler.py       # création et vérification des tokens JWT
│   ├── core/
│   │   └── logger.py             # configuration des logs
│   ├── database/
│   │   └── db.py                 # création de la base SQLite audit.db
│   ├── logs/
│   │   └── audit.log             # journal d’audit
│   ├── routes/
│   │   ├── auth.py               # POST /login
│   │   ├── health.py             # GET /health
│   │   ├── scan.py               # GET /scan
│   │   ├── nmap_scan.py          # POST /nmap_scan + suivi de job
│   │   ├── history.py            # GET /history
│   │   ├── stats.py              # GET /stats
│   │   ├── report.py             # GET /report et /report/{scan_id}
│   │   └── delete_scans.py       # DELETE /delete_scans/{scan_id}
│   ├── services/
│   │   ├── scanner.py            # logique de scan classique
│   │   ├── nmap_scanner.py       # intégration Nmap et évaluation des risques
│   │   ├── report_generator.py   # génération des PDF
│   │   └── test_scanner.py       # script de test manuel
│   └── main.py                   # point d’entrée FastAPI
├── frontend/
│   └── pages/
│       ├── index.html
│       ├── dashboard.html
│       └── history.html
└── requirements.txt
```

## Stack technique

- Backend : FastAPI + Uvicorn
- Authentification : JWT (python-jose)
- Scan réseau : Nmap via `python-nmap`
- Génération de rapports : ReportLab
- Base de données : SQLite
- Frontend : pages HTML statiques

## Prérequis

- Python 3.10+
- `pip`
- Nmap installé et disponible dans le `PATH`
- Git

## Installation

```bash
pip install -r requirements.txt
```

## Lancer l’application

### Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

Le serveur démarre ensuite sur :
- http://127.0.0.1:8000

### Frontend

```bash
cd frontend
python -m http.server 5500
```

Le frontend est accessible sur :
- http://localhost:5500

### Documentation API

Une fois le backend lancé :
- Swagger UI : http://127.0.0.1:8000/docs
- ReDoc : http://127.0.0.1:8000/redoc

## Endpoints principaux

| Méthode | Endpoint | Description |
|---|---|---|
| POST | `/login` | Authentification utilisateur |
| GET | `/scan?host={host}` | Lance un scan sur une cible |
| POST | `/nmap_scan` | Déclenche un scan Nmap en arrière-plan |
| GET | `/nmap_scan/{job_id}` | Vérifie l’état d’un job |
| GET | `/history` | Récupère l’historique des scans |
| GET | `/stats` | Retourne les statistiques générales |
| GET | `/report` | Télécharge le rapport PDF global |
| GET | `/report/{scan_id}` | Télécharge le rapport d’un scan précis |
| DELETE | `/delete_scans/{scan_id}` | Supprime un scan |
| GET | `/health` | Vérifie l’état du service et de la base |

## Base de données

Le projet utilise SQLite avec la base `audit.db` créée automatiquement au démarrage si elle n’existe pas.

Les données principales stockées dans la table `scans` sont :
- `id`
- `host`
- `type`
- `ports`
- `risque`
- `score`
- `date_scan`
- `service`
- `detected_version`
- `cve`
- `severity`
- `description`

## Notes importantes

- Les identifiants par défaut doivent être modifiés en production.
- Le secret JWT est actuellement défini dans [backend/auth/auth_handler.py](backend/auth/auth_handler.py).
- Pour les scans réseau, il faut respecter la législation et les droits d’utilisation.
- Si Nmap n’est pas disponible, l’application affiche un avertissement au démarrage.

## Développement

Pour tester ou développer :
1. Vérifier que les dépendances sont installées
2. Lancer le backend en mode développement
3. Tester les routes via `/docs`
4. Vérifier les logs dans [backend/logs](backend/logs)

4. Ensure code follows project conventions

### O2. Reporting Issues
- Describe the issue clearly
- Include steps to reproduce
- Provide relevant log outputs
- Specify your environment (OS, Python version)

## P. License & Legal

This project is developed for educational purposes in a Professional Situation (2025-2026) context. 

**Legal Notice**: Network scanning can be illegal or unethical if performed without explicit authorization. Always:
- Obtain proper authorization before scanning any network or host
- Comply with applicable laws and regulations in your jurisdiction
- Use this tool responsibly for legitimate security testing only
- Review your organization's security policies

---

**Last Updated**: 2026-06-13