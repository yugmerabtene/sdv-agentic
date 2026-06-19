# Lab 4 — Supervisor Multi-Agent avec Opencode

**Objectif :** Configurer une équipe d'agents opencode avec un Supervisor qui délègue à des spécialistes.

**Durée :** 3h

---

## Étape 1 — Créer le projet

```bash
mkdir supervisor-agent && cd supervisor-agent
```

## Étape 2 — Configurer l'équipe

`opencode.json` :

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/big-pickle",
  "default_agent": "scrum-master",
  "instructions": ["AGENTS.md"],
  "skills": {"paths": [".opencode/skills"]},
  "agent": {
    "scrum-master": {
      "mode": "primary",
      "description": "Supervisor — analyse, délègue, consolide",
      "skills": ["common", "scrum_master"]
    },
    "backend-dev": {
      "mode": "subagent",
      "description": "Développe la logique métier et les APIs",
      "skills": ["common", "backend"]
    },
    "frontend-dev": {
      "mode": "subagent",
      "description": "Crée les interfaces utilisateur",
      "skills": ["common", "frontend"]
    },
    "data-dev": {
      "mode": "subagent",
      "description": "Gère la base de données et le RAG (Retrieval-Augmented Generation)",
      "skills": ["common", "data"]
    }
  }
}
```

## Étape 3 — Créer les skills spécialisées

**`.opencode/skills/scrum_master.md`**

```markdown
# Rôle : Supervisor

Tu es le Scrum Master. Tu coordonnes une équipe de 3 développeurs.

## Workflow
1. Analyse la demande utilisateur
2. Décompose en tâches indépendantes
3. Délègue chaque tâche au sous-agent compétent
4. Consolide les résultats
5. Présente une synthèse

## Sous-agents disponibles
- @backend-dev : APIs, logique métier, auth
- @frontend-dev : HTML (HyperText Markup Language), CSS, templates
- @data-dev : Base de données, RAG, embeddings
```

**`.opencode/skills/backend.md`**

```markdown
# Rôle : Développeur Backend

Stack : FastAPI, SQLAlchemy, Pydantic, Alembic

Tu développes les APIs REST, la logique métier,
l'authentification et la validation des données.
```

**`.opencode/skills/frontend.md`**

```markdown
# Rôle : Développeur Frontend

Stack : Jinja2, Tailwind CSS, HTMX

Tu crées les interfaces utilisateur responsives,
les formulaires et les pages.
```

**`.opencode/skills/data.md`**

```markdown
# Rôle : Développeur Data

Stack : SQLite, Chroma, embeddings

Tu gères le schéma de base de données, les migrations,
les index vectoriels pour le RAG.
```

## Étape 4 — AGENTS.md

```markdown
# Équipe multi-agent

| Agent | Rôle |
|---|---|
| scrum-master | Supervisor — coordonne l'équipe |
| backend-dev | APIs et logique métier |
| frontend-dev | Interfaces utilisateur |
| data-dev | Base de données et RAG |

## Utilisation

Donnez une tâche au scrum-master. Il la décomposera
et déléguera aux sous-agents appropriés.
```

## Étape 5 — Tester la délégation

Lancez opencode et essayez :

```
"Crée une application FastAPI avec une route /hello qui retourne du JSON"
"Ajoute une page HTML pour afficher le message"
"Ajoute une base de données SQLite avec une table visites"
```

Le scrum-master devrait déléguer :
- La route `/hello` → `@backend-dev`
- La page HTML → `@frontend-dev`
- La table visites → `@data-dev`

## Étape 6 — Ajouter des tests

Demandez au scrum-master :

```
"Ajoute des tests pour chaque composant de l'application"
"Vérifie que le scrum-master délègue correctement en regardant les logs"
```

## Validation

- [ ] Le scrum-master analyse et décompose la demande
- [ ] Chaque sous-agent reçoit des tâches adaptées à son rôle
- [ ] Les sous-agents produisent du code cohérent entre eux
- [ ] L'application finale fonctionne (backend + frontend + DB)

## Pour aller plus loin

- Ajoutez un agent `tester` dédié à la qualité
- Ajoutez un agent `devops` pour Docker/CI-CD
- Créez un scénario de débogage où le scrum-master coordinateur détecte et corrige une incohérence
