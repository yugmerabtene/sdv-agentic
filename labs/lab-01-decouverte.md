# Lab 1 — Premier Projet Opencode

**Objectif :** Configurer votre premier projet opencode avec une équipe d'agents et interagir avec eux.

**Durée :** 1h

---

## Étape 1 — Initialisation

```bash
mkdir mon-premier-agent && cd mon-premier-agent
git init
```

## Étape 2 — Configurer opencode

Créez `opencode.json` :

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/big-pickle",
  "default_agent": "scrum-master",
  "instructions": [],
  "skills": {
    "paths": [".opencode/skills"]
  },
  "agent": {
    "scrum-master": {
      "mode": "primary",
      "description": "Chef de projet qui coordonne les travaux",
      "skills": ["common"]
    },
    "developer": {
      "mode": "subagent",
      "description": "Développe le code Python",
      "skills": ["common"]
    }
  }
}
```

## Étape 3 — Créer les skills

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

## Étape 4 — Créer AGENTS.md

```markdown
# Équipe

| Agent | Rôle |
|---|---|
| scrum-master | Chef de projet |
| developer | Développeur Python |

## Utilisation

Demandez au scrum-master de réaliser des tâches simples.
```

## Étape 5 — Interagir

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

## Validation

- [ ] opencode répond et exécute les instructions
- [ ] Les fichiers `hello.py` et `test_hello.py` existent
- [ ] `python hello.py` affiche le message attendu
- [ ] `pytest test_hello.py` passe

## Pour aller plus loin

- Ajoutez un agent `devops` avec Docker
- Ajoutez une skill `scrum_master.md` qui décrit comment découper des tâches
- Testez le changement d'agent : `opencode -a developer`
