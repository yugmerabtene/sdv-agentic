# CAHIER DES CHARGES
## Application Web Sociale Simplifiée

Version : MVP (Minimum Viable Product)

---

# 1. Présentation du projet

Le projet consiste à développer une application web sociale simplifiée inspirée des fonctionnalités essentielles d'un mur public de type Twitter ou Facebook.

L'objectif est de proposer une première version fonctionnelle permettant aux utilisateurs de créer un compte, se connecter et publier des messages visibles par l'ensemble des utilisateurs de la plateforme.

Cette première version doit rester volontairement simple, sans fonctionnalités avancées ou superflues.

L'application devra être entièrement conteneurisée au sein d'un unique conteneur Docker afin de simplifier son déploiement et son exploitation.

---

# 2. Objectifs du projet

L'application devra permettre :

- la création de comptes utilisateurs ;
- l'authentification des utilisateurs ;
- la gestion des utilisateurs ;
- la publication de messages sur un mur public ;
- l'affichage chronologique des publications ;
- la suppression des publications autorisées ;
- l'administration minimale de la plateforme ;
- le déploiement simplifié grâce à Docker ;
- l'automatisation complète des contrôles qualité via une chaîne CI/CD (Continuous Integration / Continuous Deployment).

---

# 3. Public cible

L'application s'adresse à :

- des utilisateurs souhaitant publier des messages courts sur un mur partagé ;
- un administrateur chargé de superviser la plateforme ;
- une équipe de développement souhaitant disposer d'une base propre pour faire évoluer le produit.

---

# 4. Périmètre fonctionnel

## 4.1 Authentification

L'application devra permettre :

### Inscription

Un utilisateur doit pouvoir créer un compte à l'aide des informations suivantes :

- nom ;
- prénom ;
- adresse email ;
- mot de passe ;
- confirmation du mot de passe.

### Connexion

Un utilisateur enregistré doit pouvoir :

- saisir son adresse email ;
- saisir son mot de passe ;
- accéder à son espace après validation.

### Déconnexion

Un utilisateur connecté doit pouvoir mettre fin à sa session.

---

## 4.2 Gestion des utilisateurs

Un utilisateur connecté doit pouvoir :

- consulter son profil ;
- modifier ses informations personnelles ;
- modifier son mot de passe ;
- supprimer son compte.

Un administrateur doit pouvoir :

- consulter la liste des utilisateurs ;
- visualiser les informations essentielles ;
- supprimer un utilisateur si nécessaire ;
- désactiver un utilisateur.

---

## 4.3 Mur public

L'application devra proposer un mur public affichant les publications.

Chaque publication devra contenir :

- son auteur ;
- son contenu ;
- sa date de publication.

Les fonctionnalités minimales attendues sont :

- créer une publication ;
- afficher les publications ;
- supprimer sa propre publication ;
- permettre à l'administrateur de supprimer n'importe quelle publication.

Les publications devront être affichées de la plus récente à la plus ancienne.

---

# 5. Fonctionnalités explicitement exclues

Afin de limiter la complexité du MVP (Minimum Viable Product), les fonctionnalités suivantes ne sont pas prévues :

- commentaires ;
- likes ;
- réactions ;
- partages ;
- abonnements ;
- système d'amis ;
- messagerie privée ;
- notifications ;
- hashtags ;
- recherche avancée ;
- publication d'images ;
- publication de vidéos ;
- fichiers joints ;
- géolocalisation ;
- application mobile ;
- API (Application Programming Interface) publique ;
- WebSocket ;
- mode temps réel.

---

# 6. Rôles utilisateurs

## Utilisateur standard

Peut :

- s'inscrire ;
- se connecter ;
- consulter le mur ;
- publier ;
- supprimer ses propres publications ;
- gérer son profil.

Ne peut pas :

- administrer la plateforme ;
- supprimer les contenus des autres utilisateurs.

---

## Administrateur

Dispose des mêmes droits qu'un utilisateur standard.

Peut également :

- consulter la liste des utilisateurs ;
- supprimer des utilisateurs ;
- désactiver des comptes ;
- supprimer toute publication.

---

# 7. Spécifications techniques

## Langage

L'application devra être développée en Python.

---

## Frontend

Le frontend devra utiliser Tailwind CSS (Cascading Style Sheets) afin de fournir :

- une interface responsive ;
- une interface simple ;
- une expérience utilisateur claire ;
- une cohérence graphique.

---

## Backend

Le backend devra assurer :

- la gestion des comptes ;
- la gestion des sessions ;
- la gestion des publications ;
- la gestion des rôles ;
- la validation des données ;
- la sécurité des accès.

---

## Base de données

Une base relationnelle légère devra être utilisée.

Pour cette première version :

- une base SQLite est suffisante ;
- aucune dépendance externe obligatoire ne devra être imposée.

---

## Conteneurisation

L'ensemble de l'application devra fonctionner dans un unique conteneur Docker.

Le conteneur devra contenir :

- le serveur Python ;
- l'application ;
- les fichiers statiques ;
- la base de données embarquée ou persistée via un volume.

Aucun autre service ne devra être nécessaire au démarrage.

---

# 8. Architecture générale attendue

L'architecture devra respecter les principes suivants :

- séparation claire des responsabilités ;
- lisibilité du code ;
- modularité ;
- maintenabilité ;
- simplicité ;
- évolutivité future.

L'architecture devra faciliter l'ajout ultérieur de nouvelles fonctionnalités.

---

# 9. Sécurité minimale

Les mesures suivantes sont obligatoires :

- mots de passe stockés de manière sécurisée ;
- validation côté serveur ;
- protection contre les injections ;
- protection contre les attaques XSS (Cross-Site Scripting) ;
- protection CSRF (Cross-Site Request Forgery) ;
- contrôle des autorisations ;
- gestion sécurisée des sessions ;
- séparation des rôles ;
- secrets externalisés ;
- absence de secrets dans le dépôt Git.

---

# 10. Exigences d'interface

L'interface devra être :

- responsive ;
- accessible ;
- lisible ;
- épurée ;
- cohérente ;
- adaptée aux écrans mobiles et desktop.

Les formulaires devront afficher des messages d'erreur explicites.

---

# 11. Exigences qualité

Le projet devra respecter les principes suivants :

- code propre ;
- conventions homogènes ;
- documentation minimale ;
- maintenabilité ;
- reproductibilité ;
- simplicité de prise en main.

---

# 12. Tests attendus

## Tests unitaires

Ils devront vérifier notamment :

- la validation des emails ;
- la validation des mots de passe ;
- la création des utilisateurs ;
- les droits d'accès ;
- la création des publications ;
- la suppression des publications.

---

## Tests d'intégration

Ils devront vérifier :

- le processus complet d'inscription ;
- le processus complet de connexion ;
- la création d'une publication ;
- la suppression d'une publication ;
- la gestion des rôles ;
- la protection des routes sécurisées.

---

## Tests fonctionnels

Ils devront couvrir :

- les parcours utilisateurs principaux ;
- les scénarios d'erreur ;
- les contrôles d'accès.

---

## Tests de non-régression

Ils devront garantir que :

- les corrections de bugs n'introduisent pas de nouvelles régressions ;
- les fonctionnalités existantes continuent de fonctionner.

Chaque correction de bug devra être accompagnée d'un test empêchant sa réapparition.

---

## Tests de sécurité

Ils devront vérifier :

- les contrôles d'accès ;
- les validations serveur ;
- les protections CSRF (Cross-Site Request Forgery) ;
- l'absence de comportements dangereux évidents.

---

# 13. Chaîne CI/CD

Une chaîne d'intégration et de déploiement continus devra être mise en place.

L'objectif est de garantir la qualité des livraisons et d'automatiser les contrôles.

---

## Déclencheurs

La chaîne CI/CD (Continuous Integration / Continuous Deployment) devra s'exécuter :

- lors d'un push ;
- lors d'une Pull Request ou Merge Request ;
- avant toute fusion vers les branches importantes ;
- avant tout déploiement.

---

## Phase 1 : Vérifications préliminaires

Avant toute construction :

- récupération du code ;
- vérification de la structure du projet ;
- installation des dépendances ;
- validation de la configuration ;
- contrôle des conventions si applicable.

---

## Phase 2 : Contrôles qualité

La chaîne devra exécuter :

- analyses statiques ;
- linting ;
- vérifications de cohérence.

Toute anomalie critique devra interrompre le pipeline.

---

## Phase 3 : Tests avant construction

Les tests suivants devront être exécutés :

- tests unitaires ;
- tests d'intégration ;
- tests de non-régression ;
- tests fonctionnels automatisés lorsque disponibles.

L'échec d'un test devra bloquer la suite du pipeline.

---

## Phase 4 : Construction

Le pipeline devra :

- construire l'application ;
- construire l'image Docker ;
- vérifier la réussite de la construction ;
- versionner les artefacts générés.

---

## Phase 5 : Tests sur l'artefact construit

Une fois l'image construite :

- démarrer l'application ;
- vérifier son démarrage ;
- contrôler son accessibilité ;
- rejouer les tests essentiels ;
- vérifier le bon fonctionnement global.

Tout échec devra interrompre le pipeline.

---

## Phase 6 : Vérifications de sécurité

Le pipeline devra effectuer :

- des contrôles de secrets ;
- des analyses de sécurité automatisées ;
- des vérifications de dépendances si disponibles.

Les vulnérabilités critiques devront empêcher la livraison.

---

## Phase 7 : Déploiement

Le déploiement devra être conditionné :

- à la réussite de toutes les étapes précédentes ;
- à la validation des règles de fusion ;
- au respect des politiques de branche.

Le déploiement devra être reproductible.

---

## Phase 8 : Vérifications post-déploiement

Après déploiement :

- contrôle de disponibilité ;
- vérification du bon démarrage ;
- tests de santé ;
- vérification des fonctionnalités critiques.

Une procédure de retour arrière devra pouvoir être envisagée en cas d'échec.

---

# 14. Politique Git

Le projet devra respecter une stratégie Git formalisée.

Les branches principales seront :

- main ;
- develop ;
- feature/* ;
- bugfix/* ;
- release/* ;
- hotfix/*.

Les fusions devront respecter les contrôles définis dans la chaîne CI/CD (Continuous Integration / Continuous Deployment).

---

# 15. Livrables attendus

Les livrables devront comprendre :

- le code source complet ;
- le Dockerfile ;
- la documentation d'installation ;
- la documentation d'exploitation ;
- la documentation de lancement ;
- le fichier de configuration CI/CD (Continuous Integration / Continuous Deployment) ;
- les tests automatisés ;
- le cahier des charges ;
- les instructions de création d'un administrateur.

---

# 16. Priorisation MVP

## Sprint 1

- Initialisation du projet ;
- Dockerisation ;
- Structure applicative.

## Sprint 2

- Inscription ;
- Connexion ;
- Déconnexion ;
- Sessions.

## Sprint 3

- Mur public ;
- Création des publications ;
- Affichage des publications ;
- Suppression des publications.

## Sprint 4

- Gestion du profil ;
- Administration des utilisateurs ;
- Gestion des rôles.

## Sprint 5

- Mise en place complète des tests ;
- Mise en place de la CI/CD (Continuous Integration / Continuous Deployment) ;
- Stabilisation ;
- Documentation ;
- Préparation à la mise en production.

---

# 17. Définition de terminé

Une fonctionnalité est considérée comme terminée lorsque :

- elle répond au besoin défini ;
- elle respecte les critères d'acceptation ;
- elle est testée ;
- elle ne génère aucune régression connue ;
- elle fonctionne dans le conteneur Docker ;
- elle respecte les exigences de sécurité ;
- elle est validée par la chaîne CI/CD (Continuous Integration / Continuous Deployment) ;
- elle est documentée lorsque nécessaire.