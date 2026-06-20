# Agentic Developer Craftsmanship

**Construisez des systèmes agentiques professionnels — de l'histoire de l'IA au déploiement en production.**

Ce cours 100% open-source vous guide pas à pas à travers les concepts et techniques du développement d'agents autonomes. Chaque chapitre contient :

- **Une section théorique** avec schémas et explications
- **Des prérequis clairs** : ce qu'il faut installer avant de commencer
- **Un TP pratique** avec fichiers à créer, commandes à exécuter, et corrigé
- **Une checklist de validation** pour vérifier votre progression

**Particularité :** aucun abonnement API requis. Tout fonctionne avec `opencode` et le modèle gratuit `big-pickle`.

**Fil rouge :** un réseau social dont le cahier des charges est dans [`projet/gestion_de_projet/cdc.md`](projet/gestion_de_projet/cdc.md). Chaque TP construit ce projet pas à pas.

---

## Parcours et progression

Le cours se découpe en **5 phases** qu'il faut suivre dans l'ordre :

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5
Fondamentaux    Interaction    Mémoire &      Production     Mise en
(P1-P2)        avec LLMs      Collaboration  (P7-P8)        pratique
               (P3-P4)        (P5-P6)                       (P9-P10)
```

---

## Prérequis général

Avant de commencer le **Chapitre 1**, installez ces outils :

```bash
# 1. Vérifier Python (>= 3.10)
python3 --version

# 2. Installer opencode
pip install opencode

# 3. Vérifier l'installation
opencode --version

# 4. Tester le modèle gratuit big-pickle
opencode -m opencode/big-pickle -t "Bonjour, quel est ton rôle ?"
```

> **Résultat attendu :** l'agent opencode répond avec une présentation.

---

## Les 10 chapitres du cours

---

### Phase 1 — Fondamentaux

#### [Chapitre 1 — Histoire & Genèse de l'IA](CHAPITRE-01-histoire-ia.md)

| | |
|---|---|
| **Théorie** | 1950 à 2026 : Turing, Transformers, ère générative, ère agentique |
| **TP** | Installer Python, opencode, big-pickle — premier agent opérationnel |
| **⏱ Durée** | 1h30 |
| **Prérequis** | Python 3.10+, pip |

```bash
# Vérifications avant de commencer
python3 --version && pip --version
```

---

#### [Chapitre 2 — Fondations des LLM](CHAPITRE-02-fondations-llm.md)

| | |
|---|---|
| **Théorie** | Tokenisation, attention, architecture Transformer, scaling laws |
| **TP** | Tokenizer un texte avec Python, visualiser les tokens |
| **⏱ Durée** | 1h30 |
| **Prérequis** | Python 3.10+, pip |

```bash
# Nouvelles dépendances pour cette chapitre
pip install tiktoken pytest
```

---

### Phase 2 — Interaction avec les LLMs

#### [Chapitre 3 — Prompt Engineering & Tool Use](CHAPITRE-03-prompt-tool-use.md)

| | |
|---|---|
| **Théorie** | System prompt, few-shot, CoT, ReAct, function calling |
| **TP** | Assistant CLI avec outils (météo, calcul) |
| **⏱ Durée** | 2h |
| **Prérequis** | Python 3.10+, pip, opencode |

```bash
# Aucune dépendance supplémentaire — Python standard suffit
```

---

#### [Chapitre 4 — Architecture Agentique](CHAPITRE-04-architecture-agent.md)

| | |
|---|---|
| **Théorie** | Boucle agent, contexte, planification, production |
| **TP** | Implémenter une boucle agent perception→raisonnement→action |
| **⏱ Durée** | 2h |
| **Prérequis** | Chapitre 3 terminée, Python, opencode |

```bash
# Aucune dépendance supplémentaire
```

---

### Phase 3 — Mémoire & Collaboration

#### [Chapitre 5 — Mémoire & RAG](CHAPITRE-05-memoire-rag.md)

| | |
|---|---|
| **Théorie** | Embeddings, vector stores, RAG, chunking, mémoire long-terme |
| **TP** | Agent avec mémoire persistante (SQLite) |
| **⏱ Durée** | 2h |
| **Prérequis** | Chapitre 4 terminée, Python, pip, opencode |

```bash
# Nouvelles dépendances pour cette chapitre
pip install chromadb sentence-transformers
```

---

#### [Chapitre 6 — Multi-Agent Orchestration](CHAPITRE-06-multi-agent.md)

| | |
|---|---|
| **Théorie** | Patterns supervisor, fan-out, débat, résilience |
| **TP** | Configurer une équipe multi-agent avec opencode |
| **⏱ Durée** | 2h |
| **Prérequis** | Chapitre 5 terminée, Python, opencode, git |

```bash
# Vérifier git
git --version
```

---

### Phase 4 — Production

#### [Chapitre 7 — MCP & Standards](CHAPITRE-07-mcp-standards.md)

| | |
|---|---|
| **Théorie** | Model Context Protocol, A2A, interopérabilité |
| **TP** | Créer un serveur MCP météo, le connecter à opencode |
| **⏱ Durée** | 2h |
| **Prérequis** | Chapitre 6 terminée, Python, pip, opencode |

```bash
# Nouvelles dépendances pour cette chapitre
pip install mcp
```

---

#### [Chapitre 8 — CI/CD & DevOps pour Agents](CHAPITRE-08-cicd-devops.md)

| | |
|---|---|
| **Théorie** | Tests d'agents, pipeline CI/CD, monitoring, coûts tokens |
| **TP** | Pipeline CI/CD complet + Scrum Board GitHub |
| **⏱ Durée** | 3h |
| **Prérequis** | Chapitre 7 terminée, Python, pip, opencode, git, compte GitHub |

```bash
# Nouvelles dépendances pour cette chapitre
pip install pytest ruff bandit

# Vérifier GitHub CLI
gh --version
```

---

### Phase 5 — Mise en pratique

#### [Chapitre 9 — Sécurité & Safety des Agents](CHAPITRE-09-securite.md)

| | |
|---|---|
| **Théorie** | Prompt injection, jailbreak, OWASP Top 10 LLM, permissions |
| **TP** | Configurer les permissions opencode, tester des injections |
| **⏱ Durée** | 1h30 |
| **Prérequis** | Chapitre 8 terminée, Python, opencode, git |

```bash
# Aucune dépendance supplémentaire
```

---

#### [Chapitre 10 — Opencode & Mise en Pratique](CHAPITRE-10-opencode-labs.md)

| | |
|---|---|
| **Théorie** | Configuration opencode, équipe d'agents, skills |
| **Lab 1** | Premier projet opencode avec 2 agents |
| **Lab 2** | Équipe complète avec CI/CD et Project Board |
| **Lab 3** | Développement complet du réseau social |
| **⏱ Durée** | 4h |
| **Prérequis** | Tous les chapitres 1-9 terminés, Python, opencode, git, GitHub |

```bash
# Vérification finale avant d'attaquer les labs
python --version && opencode --version && git --version && gh --version
```

---

## Stack technique

| Outil | Rôle | Coût |
|---|---|---|
| [opencode](https://opencode.ai) | Plateforme agentic | Gratuit |
| `opencode/big-pickle` | Modèle LLM gratuit | Gratuit |
| Python 3.10+ | Langage de développement | Gratuit |
| SQLite | Base de données embarquée | Gratuit |
| Docker | Conteneurisation | Gratuit |
| GitHub Actions | CI/CD | Gratuit |

---

## Comment utiliser ce cours

1. **Suivez l'ordre** — chaque chapitre suppose les connaissances de la précédente
2. **Lisez la théorie** — les concepts sont illustrés de schémas et d'exemples
3. **Faites les prérequis** — les commandes d'installation sont en tête de chaque chapitre
4. **Réalisez le TP** — fichiers à créer, commandes à exécuter, résultat attendu
5. **Validez avec la checklist** — tout est vert ? Passez à la suite

---

## Projet fil rouge — Réseau social

Chaque TP construit une pièce du projet final défini dans le
[**Cahier des Charges**](projet/gestion_de_projet/cdc.md).

| Chapitre | Contribution au projet |
|--------|----------------------|
| P1 | Environnement opencode configuré |
| P2 | Compréhension des tokens et du contexte |
| P3 | Assistant CLI avec outils |
| P4 | Boucle agent pour interagir avec la base de données |
| P5 | Mémoire persistante pour le fil d'actualité |
| P6 | Équipe d'agents backend/frontend/data |
| P7 | Serveur MCP pour exposer les APIs du réseau social |
| P8 | Pipeline CI/CD qui teste et déploie l'application |
| P9 | Permissions et sécurité des agents |
| P10 | **Projet complet développé par l'équipe d'agents** |

---

## Ressources

- [Scrum Board — Suivi de progression](https://github.com/users/yugmerabtene/projects/13)
- [Documentation opencode](https://opencode.ai)
- [Cahier des charges du projet](projet/gestion_de_projet/cdc.md)
