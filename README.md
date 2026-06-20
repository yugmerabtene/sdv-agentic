# SDV-Agentic-Dev

Cours 100% open-source sur le developpement de **systemes agentiques** — de l'histoire de l'IA (Intelligence Artificielle) a la mise en production d'agents autonomes avec opencode + `opencode/big-pickle` (zero API payante).

Projet fil rouge : application web sociale simplifiee definie dans [`projet/gestion_de_projet/cdc.md`](projet/gestion_de_projet/cdc.md).

---

## Sommaire

### [Partie 1 — Histoire & Genese de l'IA](PARTIE-01-histoire-ia.md)
Fondements, Transformers, ere generative, ere agentique, panorama 2026.
- 1.1-1.6 : Les fondations (1950-2012)
- 2.1-2.5 : La rupture Transformer (attention, scalabilite)
- 3.1-3.4 : L'ere generative (GPT-3, RLHF, GPT-4)
- 4.1-4.7 : L'ere agentique (tool use, ReAct, memoire, multi-agent, MCP, opencode)
- 5.1-5.3 : Panorama 2026 (acteurs, benchmarks, limites)

### [Partie 2 — Fondations des LLM (Large Language Model)](PARTIE-02-fondations-llm.md)
Fonctionnement interne des modeles de langage.
- 1 : Tokenisation
- 2 : Mecanisme d'attention
- 3 : Architecture Transformer
- 4 : Scaling laws
- 5 : Processus de generation
- 6 : Types de modeles (proprietaire vs open-source)

### [Partie 3 — Prompt Engineering & Tool Use](PARTIE-03-prompt-tool-use.md)
Maitriser les invites et les appels d'outils.
- 1 : Fondamentaux du prompt (system, user, few-shot)
- 2 : Techniques de prompting (CoT, ReAct)
- 3 : Tool use & function calling
- 4 : Pattern ReAct
- 5 : Systeme de prompt pour agent
- 6 : TP — Assistant CLI avec outils

### [Partie 4 — Architecture Agentique](PARTIE-04-architecture-agent.md)
Concevoir un agent autonome.
- 1 : Qu'est-ce qu'un agent ?
- 2 : La boucle agent (percevoir, raisonner, agir)
- 3 : Gestion du contexte
- 4 : Planification
- 5 : Architecture en production

### [Partie 5 — Memoire & RAG (Retrieval-Augmented Generation)](PARTIE-05-memoire-rag.md)
Donner de la memoire aux agents.
- 1 : Types de memoire (court-terme, long-terme, ephemere)
- 2 : Embeddings & vectorisation
- 3 : Vector stores (Chroma, FAISS)
- 4 : RAG — Retrieval-Augmented Generation
- 5 : Strategies de chunking
- 6 : Memoire long-terme pour agents
- 7 : TP — Agent avec memoire persistante

### [Partie 6 — Multi-Agent Orchestration](PARTIE-06-multi-agent.md)
Coordonner plusieurs agents specialises.
- 1 : Pourquoi plusieurs agents ?
- 2 : Patterns de communication (supervisor, fan-out, debat)
- 3 : Architecture Supervisor
- 4 : Gestion asynchrone & files d'attente
- 5 : Erreurs & resilience
- 6 : TP — Supervisor multi-agent avec opencode

### [Partie 7 — MCP (Model Context Protocol) & Standards](PARTIE-07-mcp-standards.md)
Standardiser les communications agentiques.
- 1 : Pourquoi des standards ?
- 2 : Architecture MCP (Modele Context Protocol)
- 3 : Creer un serveur MCP avec Python
- 4 : A2A — Agent-to-Agent Protocol
- 5 : Standards dans le monde opencode
- 6 : Interoperabilite avec opencode
- 7 : TP — Serveur MCP

### [Partie 8 — CI/CD & DevOps pour Agents](PARTIE-08-cicd-devops.md)
Mettre en production des agents.
- 1 : Pourquoi la CI/CD est cruciale
- 2 : Tester des agents (unitaires, integration, benchmarks)
- 3 : Pipeline CI/CD pour agents
- 4 : Monitoring & observabilite
- 5 : Gestion des couts tokens
- 6 : TP — CI/CD pour projet agentique

### [Partie 9 — Securite & Safety des Agents](PARTIE-09-securite.md)
Proteger les systemes agentiques.
- 1 : Risques specifiques aux agents
- 2 : Prompt injection
- 3 : Jailbreak
- 4 : Autorisations & permissions
- 5 : OWASP Top 10 pour LLMs
- 6 : Bonnes pratiques pour agents opencode

### [Partie 10 — Opencode & Mise en Pratique](PARTIE-10-opencode-labs.md)
Configurer et executer une equipe d'agents.
- 1 : Qu'est-ce qu'opencode ?
- 2 : Configuration d'un projet opencode
- 3 : Utiliser opencode en ligne de commande
- 4 : Labs pratiques (decouverte, equipe Scrum)
- 5 : Evaluation & validation

---

## Stack technique

| Outil | Role | Cout |
|---|---|---|
| [opencode](https://opencode.ai) | Plateforme agentic | Gratuit |
| `opencode/big-pickle` | Modele LLM gratuit | Gratuit |
| Python | Langage de developpement | Gratuit |
| SQLite / Docker / GitHub Actions | Base de donnees, conteneurisation, CI/CD | Gratuit |
