# Partie 10 — Opencode & Mise en Pratique Agentique

## Objectifs pédagogiques

- Configurer un projet opencode de A à Z
- Créer une équipe d'agents spécialisés
- Rédiger des skills efficaces
- Orchestrer un projet via agents Scrum
- Réaliser les labs pratiques

---

## 1. Qu'est-ce qu'opencode ?

[**opencode**](https://opencode.ai) est une plateforme agentic open-source qui transforme un LLM (Large Language Model) en équipe de développement collaborative.

### 1.1 Principe

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#7c3aed',
  'primaryTextColor': '#fff',
  'lineColor': '#a78bfa'
}}}%%
graph TD
    U[Utilisateur] --> SM[Scrum Master<br/>Agent principal]
    SM --> DEV[Développeur<br/>Sous-agent]
    SM --> OPS[DevOps<br/>Sous-agent]
    SM --> QA[Tester<br/>Sous-agent]
    
    DEV --> C[Code produit]
    OPS --> I[Infrastructure]
    QA --> T[Tests validés]
    
    C --> SM
    I --> SM
    T --> SM
    SM --> U
    
    style U fill:#7c3aed,color:#fff,stroke:#5b21b6
    style SM fill:#0891b2,color:#fff,stroke:#155e75
    style DEV fill:#059669,color:#fff,stroke:#047857
    style OPS fill:#d97706,color:#fff,stroke:#b45309
    style QA fill:#dc2626,color:#fff,stroke:#b91c1c
    style C fill:#1e293b,color:#f1f5f9,stroke:#334155
    style I fill:#1e293b,color:#f1f5f9,stroke:#334155
    style T fill:#1e293b,color:#f1f5f9,stroke:#334155
```

### 1.2 Avantages

| Avantage | Description |
|---|---|
| **Gratuit** | opencode + big-pickle = 0€ |
| **Open-source** | Code visible, modifiable, auto-hébergeable |
| **Équipe intégrée** | Scrum Master, Dev, DevOps, Tester prêts à l'emploi |
| **Skills modulaires** | Prompts spécialisés chargés selon le contexte |
| **MCP (Model Context Protocol) natif** | Support du Model Context Protocol |
| **Fichier de config unique** | Tout est dans `opencode.json` |

---

## 2. Configuration d'un Projet opencode

### 2.1 Structure minimale

```
mon-projet-agentic/
├── opencode.json        ← Configuration des agents
├── AGENTS.md            ← Documentation de l'équipe
└── .opencode/
    └── skills/          ← Prompts spécialisés
        ├── common.md
        └── scrum_master.md
```

### 2.2 `opencode.json`

Créez un fichier `opencode.json` :

```jsonc
{
  "$schema": "https://opencode.ai/config.json",  // Schéma de validation du fichier
  "model": "opencode/big-pickle",  // Modèle gratuit — aucun coût
  "default_agent": "scrum-master",  // Agent principal par défaut
  "instructions": ["AGENTS.md"],  // Documentation de l'équipe
  "skills": {
    "paths": [".opencode/skills"]  // Dossier des compétences spécialisées
  },
  "agent": {
    "scrum-master": {
      "mode": "primary",  // Agent principal, coordinateur
      "description": "Coordonne l'équipe, découpe le travail en tâches",
      "skills": ["common", "scrum_master"]
    },
    "developer": {
      "mode": "subagent",  // Sous-agent délégué
      "description": "Écrit le code, les tests, la documentation",
      "skills": ["common", "developer"]
    },
    "devops": {
      "mode": "subagent",
      "description": "Docker, CI/CD (Continuous Integration / Continuous Deployment), déploiement",
      "skills": ["common", "devops"]
    },
    "tester": {
      "mode": "subagent",
      "description": "Tests unitaires, intégration, qualité",
      "skills": ["common", "tester"]
    }
  }
}
```

### 2.3 `AGENTS.md`

Créez un fichier `AGENTS.md` :

```markdown
# Équipe de développement

| Agent                  | Rôle                               | Mode      |
|------------------------|------------------------------------|-----------|
| scrum-master           | Chef de projet — planifie, coordonne| primary   |
| developer              | Développe le code                  | subagent  |
| devops                 | Infrastructure, CI/CD              | subagent  |
| tester                 | Tests et qualité                   | subagent  |

## Workflow
1. L'utilisateur donne une instruction
2. Le scrum-master analyse et découpe en tâches
3. Les tâches sont déléguées aux sous-agents via `task()`
4. Chaque sous-agent produit le résultat
5. Le scrum-master consolide et présente
```

### 2.4 Skills

**`.opencode/skills/common.md`**
```markdown
# Connaissances communes

Langage : Python
Framework : FastAPI
Base de données : SQLite
Conteneurisation : Docker
Tests : pytest
Qualité : ruff, mypy

L'équipe communique en français.
Le code est en anglais (variables, commentaires).
```

**`.opencode/skills/scrum_master.md`**
```markdown
# Rôle du Scrum Master

Tu es le Scrum Master. Tu coordonnes l'équipe.

## Responsabilités
1. Analyser la demande utilisateur
2. Consulter les documents de référence
3. Découper en user stories et tâches
4. Déléguer aux sous-agents compétents
5. Vérifier la qualité du livrable
6. Présenter une synthèse à l'utilisateur

## Format de réponse
- Analyse rapide du besoin
- Actions réalisées
- Vérifications effectuées
- Risques identifiés
- Recommandations
```

---

## 3. Utiliser opencode en Ligne de Commande

### 3.1 Commandes de base

```bash
# Démarrer opencode
opencode

# Changer d'agent
opencode --agent developer
opencode -a devops

# Mode tâche (sans interaction)
opencode --task "Ajoute une route /health"
opencode -t "Lance les tests"

# Voir la configuration
opencode --config
```

### 3.2 Workflow typique

```bash
# 1. L'utilisateur donne une instruction
> "Initialise le projet FastAPI avec Docker"

# 2. Le scrum master analyse et délègue
> "J'analyse la demande... Je délègue au developer et au devops."

# 3. Les sous-agents produisent le code
# 4. Le scrum master vérifie et synthétise
# 5. Résultat livré à l'utilisateur
```

### 3.3 Délégation entre agents

Dans le fichier de configuration, les agents peuvent déléguer des tâches :

```
@developer: Crée la structure du projet FastAPI
@devops: Ajoute le Dockerfile
@tester: Vérifie que les tests passent
```

---

## 4. Labs Pratiques

### 4.1 Lab 1 — Premier Projet Opencode

> **Projet fil rouge** : ce lab final configure opencode pour developper l'ensemble du reseau social defini dans [`projet/gestion_de_projet/cdc.md`](projet/gestion_de_projet/cdc.md) avec une equipe d'agents Scrum.

**Objectif :** Configurer votre premier projet opencode avec une équipe d'agents et interagir avec eux.

**Durée :** 1h

---

#### Étape 1 — Initialisation

```bash
mkdir mon-premier-agent && cd mon-premier-agent
git init
```

#### Étape 2 — Configurer opencode

Créez `opencode.json` :

```jsonc
{
  "$schema": "https://opencode.ai/config.json",  // Schéma de validation
  "model": "opencode/big-pickle",  // Modèle gratuit
  "default_agent": "scrum-master",  // Agent principal par défaut
  "instructions": [],  // Instructions complémentaires (optionnel)
  "skills": {
    "paths": [".opencode/skills"]  // Dossier des compétences
  },
  "agent": {
    "scrum-master": {
      "mode": "primary",  // Agent coordinateur principal
      "description": "Chef de projet qui coordonne les travaux",
      "skills": ["common"]
    },
    "developer": {
      "mode": "subagent",  // Sous-agent d'exécution
      "description": "Développe le code Python",
      "skills": ["common"]
    }
  }
}
```

#### Étape 3 — Créer les skills

Créez `.opencode/skills/common.md` :

```markdown
# Projet de démonstration

Langage : Python 3.12
Outil : opencode avec big-pickle (modèle gratuit)

Conventions :
- Code en anglais
- Communication en français
- Tests avec pytest
```

#### Étape 4 — Créer AGENTS.md

```markdown
# Équipe

| Agent | Rôle |
|---|---|
| scrum-master | Chef de projet |
| developer | Développeur Python |

## Utilisation

Demandez au scrum-master de réaliser des tâches simples.
```

#### Étape 5 — Interagir

Lancez opencode :

```bash
opencode
```

Essayez ces instructions :

```
"Crée un fichier hello.py qui affiche 'Bonjour depuis un agent'"
"Exécute le fichier avec Python"
"Crée un test pour ce fichier"
```

#### Validation

- [ ] opencode répond et exécute les instructions
- [ ] Les fichiers `hello.py` et `test_hello.py` existent
- [ ] `python hello.py` affiche le message attendu
- [ ] `pytest test_hello.py` passe

#### Pour aller plus loin

- Ajoutez un agent `devops` avec Docker
- Ajoutez une skill `scrum_master.md` qui décrit comment découper des tâches
- Testez le changement d'agent : `opencode -a developer`

---

## 5. Évaluation & Validation

### 5.1 Critères pour chaque lab

| Critère | Description |
|---|---|
| **Fonctionnalité** | Le lab répond au besoin défini |
| **Qualité code** | ruff, mypy passent |
| **Tests** | pytest passe |
| **Docker** | Fonctionne dans un conteneur |
| **Documentation** | README à jour |

### 5.2 Auto-évaluation

```bash
# Vérification rapide
opencode -t "Vérifie la qualité du code"
opencode -t "Exécute les tests"
opencode -t "Vérifie que le Dockerfile est valide"
```

---

## Points clés à retenir

1. **opencode** transforme un LLM en équipe de développement collaborative
2. La configuration se fait via `opencode.json`, `AGENTS.md` et des **skills**
3. Les agents communiquent par **délégation** (`@agent`, `task()`)
4. Les **labs** sont des exercices progressifs pour maîtriser l'agentic
5. Tout est **gratuit et open-source** avec opencode + big-pickle

---

## Liens

- [Partie 1 — Histoire de l'IA (Intelligence Artificielle)](./PARTIE-01-histoire-ia.md)
- [Partie 4 — Architecture Agentique](./PARTIE-04-architecture-agent.md)
- [Partie 7 — MCP & Standards](./PARTIE-07-mcp-standards.md)
- [Documentation opencode](https://opencode.ai)
