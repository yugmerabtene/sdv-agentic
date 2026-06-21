# Agentic Developer Craftsmanship

**Construisez des systèmes agentiques professionnels — de l'histoire de l'Intelligence Artificielle au déploiement en production.**

Ce cours 100% open-source vous guide à travers les concepts et techniques du développement d'agents autonomes. Chaque chapitre contient :

- **Une section théorique** avec schémas et explications
- **Des prérequis clairs** : ce qu'il faut installer avant de commencer
- **Un TP pratique** avec fichiers à créer, commandes à exécuter, et corrigé
- **Une checklist de validation** pour vérifier votre progression

**Particularité :** aucun abonnement API (Application Programming Interface) requis. Tout fonctionne avec `opencode` et le modèle gratuit `big-pickle`.

**Fil rouge :** un réseau social dont le cahier des charges est dans [`projet/gestion_de_projet/cdc.md`](projet/gestion_de_projet/cdc.md). Chaque TP construit ce projet progressivement.

---

## Parcours et progression

Le cours se découpe en **5 phases** qu'il faut suivre dans l'ordre :

```
Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 4 ──► Phase 5
Mise à jour    Interaction    Mémoire &      Production     Mise en
(P1-P2)        avec LLMs      Collaboration  (P7-P8)        pratique
               (P3-P4)        (P5-P6)                       (P9-P10)
```

---

## Prérequis général

Avant de commencer le **Chapitre 1**, installez ces outils :

### Linux (Ubuntu/Debian)

```bash
# 1. Mettre à jour les paquets
sudo apt update

# 2. Installer Python, pip, Git et Docker
sudo apt install python3 python3-pip python3-venv git docker.io -y

# 3. Autoriser l'utilisateur courant à lancer Docker sans sudo
sudo usermod -aG docker "$USER"

# 4. Redémarrer la session, puis vérifier Docker
docker --version
docker run hello-world

# 5. Installer opencode
python3 -m pip install --user opencode

# 6. Vérifier les outils
python3 --version
python3 -m pip --version
git --version
docker --version
opencode --version

# 7. Tester le modèle gratuit big-pickle
opencode -m opencode/big-pickle -t "Bonjour, quel est ton rôle ?"
```

### macOS

```bash
# 1. Installer Homebrew si nécessaire : https://brew.sh

# 2. Installer Python, Git et Docker Desktop
brew install python git
brew install --cask docker

# 3. Ouvrir Docker Desktop une première fois, puis vérifier Docker
open -a Docker
docker --version
docker run hello-world

# 4. Installer opencode
python3 -m pip install --user opencode

# 5. Vérifier les outils
python3 --version
python3 -m pip --version
git --version
docker --version
opencode --version

# 6. Tester le modèle gratuit big-pickle
opencode -m opencode/big-pickle -t "Bonjour, quel est ton rôle ?"
```

### Windows 10/11 (PowerShell)

```powershell
# 1. Installer Python, Git et Docker Desktop avec winget
winget install Python.Python.3.12
winget install Git.Git
winget install Docker.DockerDesktop

# 2. Redémarrer Windows, lancer Docker Desktop, puis vérifier Docker
docker --version
docker run hello-world

# 3. Installer opencode
py -m pip install --user opencode

# 4. Vérifier les outils
py --version
py -m pip --version
git --version
docker --version
opencode --version

# 5. Tester le modèle gratuit big-pickle
opencode -m opencode/big-pickle -t "Bonjour, quel est ton rôle ?"
```

> **Résultat attendu :** Python, Git, Docker et opencode affichent une version. `docker run hello-world` affiche un message de succès. L'agent opencode répond avec une présentation.

### Convention de commandes pour tout le cours

| Usage | Linux/macOS | Windows PowerShell |
|---|---|---|
| Lancer Python | `python3 script.py` | `py script.py` |
| Installer un paquet | `python3 -m pip install paquet` | `py -m pip install paquet` |
| Lancer pytest | `python3 -m pytest tests/ -v` | `py -m pytest tests/ -v` |
| Commandes Git | `git ...` | `git ...` |
| Commandes Docker | `docker ...` | `docker ...` |
| Commandes opencode | `opencode ...` | `opencode ...` |

Dans les chapitres, si une commande est écrite avec `python3`, utilisez `py` sous Windows PowerShell. Exemple : `python3 agent.py` devient `py agent.py`.

### Convention de dossiers pour tous les TPs

Quand un TP commence par une commande comme `mkdir mon-projet && cd mon-projet`, cela signifie :

1. Ouvrez un terminal dans le dossier où vous rangez vos exercices, par exemple `~/agentic-labs` sur Linux/macOS ou `C:\Users\VotreNom\agentic-labs` sur Windows.
2. Créez un **nouveau dossier de TP** avec `mkdir`.
3. Entrez dans ce dossier avec `cd`.
4. Tous les fichiers indiqués ensuite doivent être créés dans ce dossier, sauf mention contraire.

Exemple Linux/macOS :

```bash
mkdir -p ~/agentic-labs
cd ~/agentic-labs
mkdir mon-tp && cd mon-tp
pwd
```

Exemple Windows PowerShell :

```powershell
mkdir $HOME\agentic-labs
cd $HOME\agentic-labs
mkdir mon-tp
cd mon-tp
pwd
```

Le résultat de `pwd` doit afficher le dossier du TP courant. C'est dans ce dossier que vous créez `opencode.json`, `AGENTS.md`, les fichiers Python et les tests.

---

## Les 10 chapitres du cours

---

### Phase 1 — Mettre à jour les paquets

#### [Chapitre 1 — Introduction](CHAPITRE-01-histoire-ia.md)

| | |
|---|---|
| **Théorie** | 1950 à 2026 : Turing, Transformers, ère générative, ère agentique |
| **TP** | Installer Python, Git, Docker, opencode, big-pickle — premier agent opérationnel |
| **⏱ Durée** | 1h30 |
| **Prérequis** | Linux, macOS ou Windows avec accès terminal |

```bash
# Vérifications avant de commencer
python3 --version && pip --version
```

---

#### [Chapitre 2 — Fondations des LLM (Large Language Model)](CHAPITRE-02-fondations-llm.md)

| | |
|---|---|
| **Théorie** | Tokenisation, attention, architecture Transformer, scaling laws |
| **TP** | Tokenizer un texte avec Python, visualiser les tokens |
| **⏱ Durée** | 1h30 |
| **Prérequis** | Python 3.10+, pip |

```bash
# Linux/macOS
python3 -m pip install tiktoken pytest

# Windows PowerShell
py -m pip install tiktoken pytest
```

---

### Phase 2 — Interaction avec les LLMs

#### [Chapitre 3 — Prompt Engineering & Tool Use](CHAPITRE-03-prompt-tool-use.md)

| | |
|---|---|
| **Théorie** | System prompt, few-shot, CoT (Chain-of-Thought), ReAct (Reasoning + Acting), function calling |
| **TP** | Assistant CLI (Command Line Interface) avec outils (météo, calcul) |
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
| **Prérequis** | Chapitre 3 terminé, Python, opencode |

```bash
# Aucune dépendance supplémentaire
```

---

### Phase 3 — Mémoire & Collaboration

#### [Chapitre 5 — Mémoire & RAG (Retrieval-Augmented Generation)](CHAPITRE-05-memoire-rag.md)

| | |
|---|---|
| **Théorie** | Embeddings, vector stores, RAG (Retrieval-Augmented Generation), chunking, mémoire long-terme |
| **TP** | Agent avec mémoire persistante (SQLite) |
| **⏱ Durée** | 2h |
| **Prérequis** | Chapitre 4 terminé, Python, pip, opencode |

```bash
# Linux/macOS
python3 -m pip install chromadb sentence-transformers

# Windows PowerShell
py -m pip install chromadb sentence-transformers
```

---

#### [Chapitre 6 — Multi-Agent Orchestration](CHAPITRE-06-multi-agent.md)

| | |
|---|---|
| **Théorie** | Patterns supervisor, fan-out, débat, résilience |
| **TP** | Configurer une équipe multi-agent avec opencode |
| **⏱ Durée** | 2h |
| **Prérequis** | Chapitre 5 terminé, Python, opencode, git |

```bash
# Vérifier git
git --version
```

---

### Phase 4 — Production

#### [Chapitre 7 — MCP (Model Context Protocol) & Standards](CHAPITRE-07-mcp-standards.md)

| | |
|---|---|
| **Théorie** | MCP (Model Context Protocol), A2A (Agent-to-Agent), interopérabilité |
| **TP** | Créer un serveur MCP (Model Context Protocol) météo, le connecter à opencode |
| **⏱ Durée** | 2h |
| **Prérequis** | Chapitre 6 terminé, Python, pip, opencode |

```bash
# Linux/macOS
python3 -m pip install mcp

# Windows PowerShell
py -m pip install mcp
```

---

#### [Chapitre 8 — CI/CD (Continuous Integration / Continuous Deployment) & DevOps pour Agents](CHAPITRE-08-cicd-devops.md)

| | |
|---|---|
| **Théorie** | Tests d'agents, pipeline CI/CD (Continuous Integration / Continuous Deployment), monitoring, coûts tokens |
| **TP** | Pipeline CI/CD (Continuous Integration / Continuous Deployment) complet + Scrum Board GitHub |
| **⏱ Durée** | 3h |
| **Prérequis** | Chapitre 7 terminé, Python, pip, opencode, git, compte GitHub |

```bash
# Linux/macOS
python3 -m pip install pytest ruff bandit

# Windows PowerShell
py -m pip install pytest ruff bandit

# Vérifier GitHub CLI
gh --version
```

---

### Phase 5 — Mise en pratique

#### [Chapitre 9 — Sécurité & Safety des Agents](CHAPITRE-09-securite.md)

| | |
|---|---|
| **Théorie** | Prompt injection, jailbreak, OWASP (Open Worldwide Application Security Project) Top 10 LLM (Large Language Model), permissions |
| **TP** | Configurer les permissions opencode, tester des injections |
| **⏱ Durée** | 1h30 |
| **Prérequis** | Chapitre 8 terminé, Python, opencode, git |

```bash
# Aucune dépendance supplémentaire
```

---

#### [Chapitre 10 — Opencode & Mise en Pratique](CHAPITRE-10-opencode-labs.md)

| | |
|---|---|
| **Théorie** | Configuration opencode, équipe d'agents, skills |
| **Lab 1** | Premier projet opencode avec 2 agents |
| **Lab 2** | Équipe complète avec CI/CD (Continuous Integration / Continuous Deployment) et Project Board |
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
| `opencode/big-pickle` | Modèle LLM (Large Language Model) gratuit | Gratuit |
| Python 3.10+ | Langage de développement | Gratuit |
| SQLite | Base de données embarquée | Gratuit |
| Docker | Conteneurisation | Gratuit |
| GitHub Actions | CI/CD (Continuous Integration / Continuous Deployment) | Gratuit |

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
| P3 | Assistant CLI (Command Line Interface) avec outils |
| P4 | Boucle agent avec mémoire de conversation |
| P5 | Mémoire persistante (SQLite) pour stocker des faits |
| P6 | Équipe multi-agent avec superviseur et agents spécialisés |
| P7 | Serveur MCP (Model Context Protocol) pour exposer des outils |
| P8 | Pipeline CI/CD (Continuous Integration / Continuous Deployment) qui teste et déploie l'application |
| P9 | Permissions et sécurité des agents |
| P10 | **Projet complet développé par l'équipe d'agents** |

---

## Ressources

- [Scrum Board — Suivi de progression](https://github.com/users/yugmerabtene/projects/13)
- [Documentation opencode](https://opencode.ai)
- [Cahier des charges du projet](projet/gestion_de_projet/cdc.md)
