# Lancement rapide

```bash
# 1. Démarrer l'application
docker compose up -d

# 2. Ouvrir dans le navigateur
# http://localhost:5000/

# 3. Créer un compte utilisateur
# Aller sur http://localhost:5000/auth/register
# Remplir : nom, prénom, email, mot de passe

# 4. Publier un message
# Se connecter puis écrire sur le mur public

# 5. Administration
# Se connecter avec le compte admin (défini dans .env)
# Accéder à http://localhost:5000/admin/users
```

## Premier démarrage

1. Copier `.env.example` vers `.env`
2. Modifier `SECRET_KEY` (obligatoire en production)
3. Définir `ADMIN_EMAIL` et `ADMIN_PASSWORD`
4. Lancer `docker compose up -d`
5. L'administrateur est créé automatiquement
