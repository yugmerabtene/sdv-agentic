# Installation

## Prérequis

- Docker (recommandé) ou Python 3.12+
- Git

## Installation avec Docker (recommandée)

```bash
# Cloner le dépôt
git clone https://github.com/yugmerabtene/nexa-cda-agentic.git
cd nexa-cda-agentic

# Copier et éditer la configuration
cp .env.example .env
# Éditer .env avec vos propres valeurs (SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD)

# Lancer l'application
docker compose up -d

# Vérifier que l'application tourne
curl http://localhost:5000/
```

## Installation sans Docker

```bash
# Cloner le dépôt
git clone https://github.com/yugmerabtene/nexa-cda-agentic.git
cd nexa-cda-agentic

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Copier et éditer la configuration
cp .env.example .env
# Éditer .env avec vos propres valeurs

# Créer le répertoire de données
mkdir -p data

# Lancer l'application
gunicorn --bind 0.0.0.0:5000 --workers 4 app.main:app
```

## Configuration

Variables d'environnement (fichier `.env`) :

| Variable | Description | Valeur par défaut |
|---|---|---|
| `SECRET_KEY` | Clé secrète pour les sessions Flask | `dev-secret-key-change-in-production` |
| `DATABASE_URL` | URI de la base de données SQLite | `sqlite:///data/app.db` |
| `ADMIN_EMAIL` | Email du compte administrateur initial | `admin@example.com` |
| `ADMIN_PASSWORD` | Mot de passe du compte administrateur initial | `Admin123!` |
