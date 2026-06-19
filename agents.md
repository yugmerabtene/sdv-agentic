# AGENTS.md — Équipe de développement

Ce projet utilise une organisation Agile (Scrum) avec des agents IA spécialisés.

---

## Équipe

| Agent | Rôle | Mode |
|---|---|---|
| `scrum-master` | Chef de projet — planifie, coordonne, découpe le CDC en sprints | **primary** (défaut) |
| `fullstack-developer` | Développe le code (backend, frontend, API (Application Programming Interface), DB) | subagent |
| `devops` | Docker, CI/CD (Continuous Integration / Continuous Deployment), déploiement, infrastructure | subagent |
| `tester` | Tests unitaires, intégration, fonctionnels, sécurité | subagent |

---

## Conventions

- **Langue** : français (communication), anglais (code technique)
- **Modèle** : `opencode/big-pickle`
- **Instructions** : `PARTIE-*.md`, `gestion_de_projet/cdc.md`
- **Skills** : `.opencode/skills/`

---

## Workflow

1. **Comprendre** la demande et le contexte (CDC, sprint concerné)
2. **Découper** en User Stories → tâches techniques
3. **Déléguer** aux sous-agents via `task()` si nécessaire
4. **Produire** le code, les tests, la configuration
5. **Vérifier** la qualité (tests, lint, sécu)
6. **Valider** le résultat par rapport au besoin initial
7. **Synthétiser** et présenter le livrable

---

## Fichiers importants

| Fichier | Utilité |
|---|---|
| `PARTIE-01-histoire-ia.md` | Introduction à l'IA (contexte) |
| `gestion_de_projet/cdc.md` | Cahier des charges complet |
