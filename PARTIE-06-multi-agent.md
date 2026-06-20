# Partie 6 — Multi-Agent Orchestration

## Objectifs pédagogiques

- Comprendre pourquoi un seul agent ne suffit pas toujours
- Maîtriser les patterns de communication entre agents
- Savoir implémenter un Supervisor Agent
- Connaître les approches asynchrones et files d'attente

---

## 1. Pourquoi Plusieurs Agents ?

### 1.1 Limites d'un agent unique

| Problème | Exemple | Solution multi-agent |
|---|---|---|
| **Spécialisation** | Un agent ne peut pas être bon en tout | Agents spécialisés par domaine |
| **Contexte** | Un seul LLM (Large Language Model) a une fenêtre limitée | Chaque agent a son propre contexte |
| **Parallélisme** | Tâches séquentielles lentes | Agents qui travaillent en parallèle |
| **Résilience** | Un agent qui échoue bloque tout | Agents redondants, fallback |
| **Modularité** | Tout le code dans une boucle | Agents indépendants et remplaçables |

### 1.2 Principe de spécialisation

Chaque agent a un **rôle précis** et un **système prompt dédié** :

```
Agent Modérateur → Analyse de toxicité, spam
Agent Résumé     → Synthèse de contenu
Agent Recherche  → RAG (Retrieval-Augmented Generation), recherche documentaire
Agent Code      → Génération et révision de code
```

---

## 2. Patterns de Communication

### 2.1 Séquentiel (Pipeline)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#6366f1',
  'primaryTextColor': '#fff',
  'lineColor': '#818cf8'
}}}%%
graph LR
    A[Agent 1<br/>Analyse] --> B[Agent 2<br/>Traitement]
    B --> C[Agent 3<br/>Synthèse]
    C --> D[Résultat]
    
    style A fill:#7c3aed,color:#fff,stroke:#5b21b6
    style B fill:#0891b2,color:#fff,stroke:#155e75
    style C fill:#059669,color:#fff,stroke:#047857
    style D fill:#2563eb,color:#fff,stroke:#1d4ed8
```

**Quand :** Tâches où chaque étape dépend de la précédente.
**Exemple :** Analyser → Résumer → Traduire

### 2.2 Fan-Out (Parallèle)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#0891b2',
  'primaryTextColor': '#fff',
  'lineColor': '#22d3ee'
}}}%%
graph TD
    C[Coordonnateur] --> A1[Agent 1]
    C --> A2[Agent 2]
    C --> A3[Agent 3]
    A1 --> R[Agrégateur]
    A2 --> R
    A3 --> R
    R --> Result[Résultat final]
    
    style C fill:#7c3aed,color:#fff,stroke:#5b21b6
    style A1 fill:#0891b2,color:#fff,stroke:#155e75
    style A2 fill:#0891b2,color:#fff,stroke:#155e75
    style A3 fill:#0891b2,color:#fff,stroke:#155e75
    style R fill:#059669,color:#fff,stroke:#047857
    style Result fill:#2563eb,color:#fff,stroke:#1d4ed8
```

**Quand :** Tâches indépendantes qui peuvent être parallélisées.
**Exemple :** Analyser 3 documents en même temps.

### 2.3 Débat

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#dc2626',
  'primaryTextColor': '#fff',
  'lineColor': '#f87171'
}}}%%
graph TD
    Q[Question] --> A1[Agent 1<br/>Pour]
    Q --> A2[Agent 2<br/>Contre]
    A1 --> D[Débat]
    A2 --> D
    D --> J[Juge<br/>Synthèse]
    J --> V[Verdict]
    
    style Q fill:#1e293b,color:#f1f5f9,stroke:#334155
    style A1 fill:#0891b2,color:#fff,stroke:#155e75
    style A2 fill:#dc2626,color:#fff,stroke:#b91c1c
    style D fill:#d97706,color:#fff,stroke:#b45309
    style J fill:#7c3aed,color:#fff,stroke:#5b21b6
    style V fill:#059669,color:#fff,stroke:#047857
```

**Quand :** Décisions complexes où plusieurs perspectives sont utiles.
**Exemple :** "Cette PR est-elle prête à être mergée ?"

### 2.4 Hiérarchique (Supervisor)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#059669',
  'primaryTextColor': '#fff',
  'lineColor': '#34d399'
}}}%%
graph TD
    SV[Supervisor Agent] --> S1[Spécialiste 1<br/>Auth]
    SV --> S2[Spécialiste 2<br/>Posts]
    SV --> S3[Spécialiste 3<br/>Admin]
    S1 --> SV
    S2 --> SV
    S3 --> SV
    SV --> U[Utilisateur]
    
    style SV fill:#7c3aed,color:#fff,stroke:#5b21b6
    style S1 fill:#0891b2,color:#fff,stroke:#155e75
    style S2 fill:#0891b2,color:#fff,stroke:#155e75
    style S3 fill:#0891b2,color:#fff,stroke:#155e75
    style U fill:#059669,color:#fff,stroke:#047857
```

**Quand :** Orchestration complexe avec délégation dynamique.
**Exemple :** Un chef de projet qui délègue à des spécialistes.

---

## 3. Architecture Supervisor

### 3.1 Principe

Le **Supervisor Agent** est un LLM qui :
1. Reçoit la demande de l'utilisateur
2. Décide quel(s) sous-agent(s) invoquer
3. Consolide les résultats
4. Planifie la prochaine action

### 3.2 Prompt du Supervisor

```
Tu es un Supervisor Agent. Tu coordonnes une équipe d'agents spécialisés.

Agents disponibles :
- moderator(content) → analyse toxicité, spam (0-1)
- summarizer(texts) → résumé de contenu
- searcher(query) → recherche dans la base de connaissances

Règles :
1. Analyse la demande de l'utilisateur
2. Décide quels agents activer (séquentiel ou parallèle)
3. Consolide les résultats
4. Si un agent échoue, replanifie
5. Réponds à l'utilisateur uniquement quand tu as le résultat final
```

### 3.3 Implémentation

Créez un fichier `supervisor_agent.py` :

```python
class SupervisorAgent:
    # Constructeur : initialise le LLM, les sous-agents et l'historique
    def __init__(self, llm):
        self.llm = llm                              # Modèle de langage principal
        self.agents = {
            "moderator": ModeratorAgent(llm),       # Agent de modération
            "summarizer": SummarizerAgent(llm),     # Agent de résumé
            "searcher": SearcherAgent(llm),         # Agent de recherche
        }
        self.history = []                           # Historique des échanges
    
    # Point d'entrée : exécute la boucle superviseur
    def run(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})  # Enregistre la requête
        
        while True:
            # Interroge le LLM avec le prompt superviseur et les outils
            response = self.llm.chat(
                self.history,
                system=self._supervisor_prompt(),
                tools=self._agent_tools()
            )
            
            if response.content:  # Réponse finale : fin de la boucle
                return response.content
            
            # Traite chaque appel d'outil délégué par le LLM
            for tc in response.tool_calls:
                agent_name = tc.function.name       # Nom du sous-agent cible
                args = json.loads(tc.function.arguments)  # Arguments de l'appel
                result = self.agents[agent_name].run(**args)  # Exécute le sous-agent
                self.history.append({                # Stocke le résultat dans l'historique
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tc.id
                })
```

---

## 4. Gestion Asynchrone & Files d'Attente

### 4.1 Problème

Un appel agent peut prendre plusieurs secondes, voire minutes. En séquentiel, l'utilisateur attend.

### 4.2 Solution : File d'attente

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#0891b2',
  'primaryTextColor': '#fff',
  'lineColor': '#22d3ee'
}}}%%
graph LR
    U[Utilisateur] -->|"Requête"| Q[File d'attente]
    Q -->|"Task 1"| W1[Worker 1]
    Q -->|"Task 2"| W2[Worker 2]
    Q -->|"Task 3"| W3[Worker 3]
    W1 -->|"Résultat"| DB[(Base de données)]
    U -->|"Poll"| DB
    U -->|"Résultat"| R
    
    style U fill:#7c3aed,color:#fff,stroke:#5b21b6
    style Q fill:#d97706,color:#fff,stroke:#b45309
    style W1 fill:#0891b2,color:#fff,stroke:#155e75
    style W2 fill:#0891b2,color:#fff,stroke:#155e75
    style W3 fill:#0891b2,color:#fff,stroke:#155e75
    style DB fill:#1e293b,color:#f1f5f9,stroke:#334155
    style R fill:#059669,color:#fff,stroke:#047857
```

### 4.3 Approche asynchrone simple

Créez un fichier `async_orchestrator.py` :

```python
import asyncio   # Bibliothèque pour la programmation asynchrone
import uuid      # Génération d'identifiants uniques

class AsyncAgentOrchestrator:
    # Initialise le dictionnaire des tâches
    def __init__(self):
        self.tasks = {}  # stocke l'état de chaque tâche par son ID
    
    # Soumet une tâche et retourne immédiatement un ID
    async def submit(self, agent_name: str, input_data: str) -> str:
        task_id = str(uuid.uuid4())                                      # Génère un ID unique
        self.tasks[task_id] = {"status": "pending", "result": None}      # État initial
        
        # Lance le traitement en arrière-plan sans bloquer
        asyncio.create_task(self._process(agent_name, input_data, task_id))
        return task_id  # L'utilisateur récupérera le résultat plus tard
    
    # Attend le résultat d'une tâche (polling)
    async def get_result(self, task_id: str):
        while self.tasks[task_id]["status"] == "pending":  # Boucle tant que la tâche est en cours
            await asyncio.sleep(0.5)                       # Pause pour éviter de surcharger le CPU
        return self.tasks[task_id]["result"]               # Retourne le résultat final
    
    # Traitement interne d'une tâche en arrière-plan
    async def _process(self, agent_name, input_data, task_id):
        try:
            self.tasks[task_id]["status"] = "running"      # Passe en cours d'exécution
            result = await self.agents[agent_name].arun(input_data)  # Appel asynchrone du sous-agent
            self.tasks[task_id]["result"] = result         # Stocke le résultat
            self.tasks[task_id]["status"] = "done"         # Marque comme terminé
        except Exception as e:
            self.tasks[task_id]["result"] = f"Error: {e}"  # Enregistre l'erreur
            self.tasks[task_id]["status"] = "failed"       # Marque comme échoué
```

---

## 5. Erreurs & Résilience

| Pattern | Description | Code |
|---|---|---|
| **Retry** | Réessayer après un échec temporaire | `retry(max=3, delay=1)` |
| **Fallback** | Agent de remplacement si le principal échoue | `agent_b if agent_a fails` |
| **Circuit Breaker** | Arrêter les appels après N échecs consécutifs | Arrêt temporaire puis reprise |
| **Timeout** | Limiter le temps d'exécution d'un agent | `asyncio.wait_for(task, timeout=30)` |
| **Graceful degradation** | Réponse partielle si un agent est indisponible | "Module X indisponible, voici le reste" |

---

## 6. Travaux Pratiques — Supervisor Multi-Agent avec Opencode

> **Projet fil rouge** : l'equipe multi-agent que vous allez configurer a pour objectif d'implementer les fonctionnalites du reseau social defini dans [`projet/gestion_de_projet/cdc.md`](projet/gestion_de_projet/cdc.md).

**Objectif :** Configurer une équipe d'agents opencode avec un Supervisor qui délègue à des spécialistes.

**Durée :** 3h

### Étape 1 — Créer le projet

```bash
mkdir supervisor-agent && cd supervisor-agent
```

### Étape 2 — Configurer l'équipe

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

### Étape 3 — Créer les skills spécialisées

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

### Étape 4 — AGENTS.md

Créez un fichier `AGENTS.md` :

```markdown
# Équipe multi-agent

| Agent                  | Rôle                               |
|------------------------|------------------------------------|
| scrum-master           | Supervisor — coordonne l'équipe     |
| backend-dev            | APIs et logique métier             |
| frontend-dev           | Interfaces utilisateur             |
| data-dev               | Base de données et RAG             |

## Utilisation

Donnez une tâche au scrum-master. Il la décomposera
et déléguera aux sous-agents appropriés.
```

### Étape 5 — Tester la délégation

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

### Étape 6 — Ajouter des tests

Demandez au scrum-master :

```
"Ajoute des tests pour chaque composant de l'application"
"Vérifie que le scrum-master délègue correctement en regardant les logs"
```

### Validation

- [ ] Le scrum-master analyse et décompose la demande
- [ ] Chaque sous-agent reçoit des tâches adaptées à son rôle
- [ ] Les sous-agents produisent du code cohérent entre eux
- [ ] L'application finale fonctionne (backend + frontend + DB (Base de données))

### Pour aller plus loin

- Ajoutez un agent `tester` dédié à la qualité
- Ajoutez un agent `devops` pour Docker/CI-CD
- Créez un scénario de débogage où le scrum-master coordinateur détecte et corrige une incohérence

---

## Points clés à retenir

1. Le **multi-agent** permet spécialisation, parallélisme et résilience
2. Les **patterns** fondamentaux : séquentiel, fan-out, débat, hiérarchique
3. Le **Supervisor Agent** est un LLM qui orchestre d'autres LLMs
4. Les **files d'attente** évitent de bloquer l'utilisateur pendant les traitements longs
5. La **résilience** (retry, fallback, timeout) est indispensable en production

---

## Liens

- [Partie 5 — Mémoire & RAG](./PARTIE-05-memoire-rag.md)
- [Partie 7 — MCP (Model Context Protocol) & Standards](./PARTIE-07-mcp-standards.md)
- [Partie 10 — Opencode & Labs](./PARTIE-10-opencode-labs.md)
