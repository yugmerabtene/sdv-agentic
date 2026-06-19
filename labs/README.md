# Labs — SdV-Agentic-Dev

> Exercices pratiques utilisant **opencode + big-pickle** (100% gratuit).
> Chaque lab est indépendant et construit sur les concepts du cours.

---

## Progression

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#6366f1',
  'primaryTextColor': '#fff',
  'lineColor': '#818cf8',
  'mainBkg': '#1e293b',
  'background': '#0f172a',
  'titleColor': '#f1f5f9'
}}}}
graph LR
    L1[Lab 1<br/>Découverte] --> L2[Lab 2<br/>Assistant CLI]
    L2 --> L3[Lab 3<br/>Agent mémoire]
    L3 --> L4[Lab 4<br/>Supervisor]
    L4 --> L5[Lab 5<br/>Serveur MCP (Model Context Protocol)]
    L5 --> L6[Lab 6<br/>CI/CD (Continuous Integration / Continuous Deployment) agents]
    
    style L1 fill:#7c3aed,color:#fff,stroke:#5b21b6
    style L2 fill:#0891b2,color:#fff,stroke:#155e75
    style L3 fill:#059669,color:#fff,stroke:#047857
    style L4 fill:#d97706,color:#fff,stroke:#b45309
    style L5 fill:#2563eb,color:#fff,stroke:#1d4ed8
    style L6 fill:#dc2626,color:#fff,stroke:#b91c1c
```

---

## Labs

| # | Lab | Concepts | Durée |
|---|---|---|---|
| 1 | [Premier projet opencode](./lab-01-decouverte.md) | Config, agents, skills | 1h |
| 2 | [Assistant CLI avec outils](./lab-02-assistant-cli.md) | Prompt, tool use, ReAct (Reasoning + Acting) | 2h |
| 3 | [Agent avec mémoire persistante](./lab-03-memoire.md) | Mémoire, SQLite, contexte | 2h |
| 4 | [Supervisor multi-agent](./lab-04-supervisor.md) | Orchestration, délégation | 3h |
| 5 | [Serveur MCP](./lab-05-mcp.md) | MCP, serveur, client | 2h |
| 6 | [CI/CD pour agents](./lab-06-cicd.md) | Tests agents, pipeline | 2h |

---

## Projet fil rouge (optionnel)

Après les labs, utilisez l'équipe d'agents opencode pour réaliser un projet complet :

> **Application sociale simplifiée** — avec authentification, mur de publications, rôles utilisateur.

Le CDC est dans `gestion_de_projet/cdc.md`. L'équipe d'agents Scrum le découpera en sprints et le réalisera.

---

## Prérequis

- opencode installé : `pip install opencode`
- Python 3.12+
- Git
- Docker (pour les labs 5-6)
