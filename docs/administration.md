# Administration

## Création d'un administrateur

L'administrateur est créé automatiquement au premier démarrage de l'application
via les variables d'environnement `ADMIN_EMAIL` et `ADMIN_PASSWORD`.

```bash
# Dans le fichier .env
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin123!
```

Si l'utilisateur existe déjà (même email), la création est ignorée.

## Interface d'administration

Accès : `/admin/users` (réservé aux administrateurs)

Fonctionnalités :
- Liste de tous les utilisateurs (nom, prénom, email, statut)
- Suppression d'un utilisateur
- Activation / désactivation d'un compte

## Gestion des utilisateurs

Un administrateur peut :
- Consulter la liste complète des utilisateurs
- Supprimer un utilisateur (ses publications sont également supprimées)
- Désactiver un compte (l'utilisateur ne peut plus se connecter)
- Supprimer toute publication sur le mur public
