# Chapitre 3 — Prompt Engineering & Tool Use

## Objectifs pédagogiques

- Maîtriser les différentes techniques de prompting
- Savoir concevoir un system prompt efficace
- Comprendre et implémenter le function calling
- Maîtriser le pattern ReAct (Reasoning + Acting)

---

## Prérequis

Avant de commencer cette chapitre, assurez-vous d'avoir :

- Terminé les **[Chapitres 1](CHAPITRE-01-histoire-ia.md)** et **[Chapitre 2](CHAPITRE-02-fondations-llm.md)** avec leurs TP
- Python 3.10+ et opencode installés
- Compris les bases de la tokenisation (P2)

### Vérification

```bash
# Tester que tout est fonctionnel
python3 --version && opencode --version
```

> **Aucune dépendance supplémentaire** pour cette chapitre — Python standard suffit.

---

## 1. Les Fondamentaux du Prompt

### 1.1 Structure d'un prompt

Un prompt (instruction donnée au modèle de langage) se compose de plusieurs éléments :

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#6366f1',
  'primaryTextColor': '#fff',
  'lineColor': '#818cf8'
}}}%%
graph LR
    subgraph Prompt
        SP[System Prompt<br/>Rôle, règles, contexte]
        UP[User Prompt<br/>Question, tâche]
        EX["Exemples (Few-shot)<br/>"]
    end
    
    SP --> LLM["LLM (Large Language Model)"]
    UP --> LLM
    EX --> LLM
    LLM --> R[Réponse]
    
    style SP fill:#7c3aed,color:#fff,stroke:#5b21b6
    style UP fill:#0891b2,color:#fff,stroke:#155e75
    style EX fill:#059669,color:#fff,stroke:#047857
    style LLM fill:#d97706,color:#fff,stroke:#b45309
    style R fill:#2563eb,color:#fff,stroke:#1d4ed8
```

### 1.2 System Prompt

Le **system prompt** (consigne de rôle et de comportement) définit le rôle, le ton et les contraintes :

```
Tu es un assistant expert en développement Python.
Tu réponds uniquement avec du code fonctionnel.
Tu expliques brièvement ton raisonnement avant chaque réponse.
```

**Bonnes pratiques :**
- Clair et direct (pas d'ambiguïté)
- Règles précises (format, longueur, ton)
- Contraintes de sécurité (ne pas exécuter de code dangereux)
- Contexte utile (utilisateur, projet, version)

### 1.3 User Prompt

Le prompt utilisateur contient la **demande spécifique** :

```
Peux-tu écrire une fonction Python qui vérifie
si un email est valide ?
```

---

## 2. Techniques de Prompting

### 2.1 Zero-shot

Donner une instruction sans exemple. Fonctionne bien pour les tâches simples.

```
Traduis en anglais : "Les agents IA sont fascinants"
→ "AI agents are fascinating"
```

### 2.2 Few-shot (apprentissage avec quelques exemples)

Fournir **2-3 exemples** avant la question. Améliore la précision pour les tâches complexes.

```
Anglais → Français
"Hello world" → "Bonjour le monde"
"Good morning" → "Bonjour"
"AI agents" → ?
```

### 2.3 CoT (Chain-of-Thought)

Demander au modèle de **raisonner étape par étape** :

```
Jean a 12 pommes. Il en donne 3 à Marie, puis en achète 5.
Combien en a-t-il maintenant ?

Raisonnement :
1. Jean commence avec 12 pommes
2. Il donne 3 à Marie : 12 - 3 = 9
3. Il achète 5 : 9 + 5 = 14
Résultat : 14 pommes
```

**Quand l'utiliser :** Problèmes mathématiques, logiques, planification, décisions multi-étapes.

### 2.4 Instruction vs Format

On peut structurer la réponse attendue :

```
Tu es un assistant de réservation.
Pour chaque demande, réponds au format JSON :
{
  "action": "réserver | annuler | consulter",
  "paramètres": { ... }
}

Demande : "Je veux réserver une table pour 2 à 20h"
```

### 2.5 Persona Pattern

Donner un rôle spécifique au modèle :

```
Tu es un DevOps senior avec 15 ans d'expérience.
Analyse ce Dockerfile et identifie les problèmes de sécurité.
```

---

## 3. Tool Use & Function Calling

### 3.1 Principe

Le LLM (Large Language Model) peut déclarer qu'il souhaite utiliser un outil externe, sans l'exécuter lui-même.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#0891b2',
  'primaryTextColor': '#fff',
  'lineColor': '#22d3ee'
}}}%%
graph TD
    U[Utilisateur] -->|"Question"| LLM[LLM]
    LLM -->|"tool_call: get_weather('Paris')"| Orchestrator[Orchestrateur]
    Orchestrator -->|"Appel API (Application Programming Interface)"| Weather[API Météo]
    Weather -->|"15°C, pluie"| Orchestrator
    Orchestrator -->|"Observation"| LLM
    LLM -->|"Réponse"| U
    
    style U fill:#7c3aed,color:#fff,stroke:#5b21b6
    style LLM fill:#0891b2,color:#fff,stroke:#155e75
    style Orchestrator fill:#059669,color:#fff,stroke:#047857
    style Weather fill:#d97706,color:#fff,stroke:#b45309
```

### 3.2 Définir un outil

Créez un fichier `tools.py` :

```python
# Liste des outils disponibles pour le LLM
# Chaque outil est défini comme un dictionnaire conforme au schema OpenAI
tools = [
    {
        "type": "function",  # Type d'outil : appel de fonction
        "function": {
            "name": "get_weather",  # Nom unique de l'outil
            # Description qui aide le LLM à décider quand utiliser cet outil
            "description": "Obtenir la météo d'une ville",
            "parameters": {
                "type": "object",  # Le paramètre est un objet JSON
                "properties": {
                    "city": {
                        "type": "string",  # Type string pour le nom de ville
                        "description": "Nom de la ville"  # Description du champ
                    }
                },
                "required": ["city"]  # Le champ city est obligatoire
            }
        }
    }
]
```

### 3.3 Appel et exécution

```
Réponse LLM : tool_call(id="call_123", name="get_weather", args={"city": "Paris"})

→ Orchestrateur exécute : get_weather("Paris") → "15°C, nuageux"

→ Envoie l'observation au LLM :
  tool_result(id="call_123", content="15°C, nuageux")

→ LLM répond : "Il fait 15°C et nuageux à Paris."
```

### 3.4 Bonnes pratiques

| Pratique | Pourquoi |
|---|---|
| Description claire de l'outil | Le LLM comprend quand l'utiliser |
| Paramètres bien typés | Moins d'erreurs d'appel |
| Gestion des erreurs | L'outil peut échouer → le LLM doit le savoir |
| Timeout | Un outil lent bloque l'agent |
| Sécurité | Vérifier les arguments avant exécution |

---

## 4. Le Pattern ReAct

### 4.1 Principe

**ReAct** (Reasoning + Acting) alterne trois étapes :

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#059669',
  'primaryTextColor': '#fff',
  'lineColor': '#34d399'
}}}%%
graph LR
    T[Thought<br/>Raisonnement] --> A[Action<br/>Appel outil]
    A --> O[Observation<br/>Résultat]
    O --> T
    
    style T fill:#7c3aed,color:#fff,stroke:#5b21b6
    style A fill:#0891b2,color:#fff,stroke:#155e75
    style O fill:#059669,color:#fff,stroke:#047857
```

1. **Thought** : Le LLM réfléchit à ce qu'il doit faire
2. **Action** : Il appelle un outil ou produit une réponse
3. **Observation** : Le résultat de l'outil est renvoyé au LLM

### 4.2 Exemple complet

```
Question : "Quel est l'écart de température entre Paris et Tokyo aujourd'hui ?"

Thought: Je dois obtenir la météo des deux villes, puis calculer la différence.
Action: get_weather("Paris")
Observation: 15°C, nuageux

Thought: J'ai la météo de Paris. Il me faut celle de Tokyo.
Action: get_weather("Tokyo")
Observation: 22°C, ensoleillé

Thought: J'ai les deux températures. L'écart est de 22 - 15 = 7°C.
Réponse: L'écart de température entre Paris (15°C) et Tokyo (22°C) est de 7°C.
```

### 4.3 Implémentation simple

Créez un fichier `agent_loop.py` :

```python
# Boucle principale du pattern ReAct
# question : entrée utilisateur, max_steps : limite d'itérations
def agent_loop(question: str, max_steps: int = 5):
    # Initialise l'historique avec la question de l'utilisateur
    messages = [{"role": "user", "content": question}]
    
    # Boucle ReAct : Thought -> Action -> Observation
    for step in range(max_steps):
        # Envoie les messages au LLM avec les outils disponibles
        response = llm.chat(messages, tools=tools)
        
        # Si le LLM répond directement, c'est la réponse finale
        if response.content:  # Réponse finale
            return response.content
        
        # Si le LLM demande un appel d'outil
        if response.tool_calls:
            # Parcourt tous les appels d'outils demandés
            for tool_call in response.tool_calls:
                result = execute_tool(tool_call)  # Exécute l'outil
                # Ajoute la demande d'appel à l'historique
                messages.append(tool_call.to_message())
                # Ajoute le résultat (observation) à l'historique
                messages.append({
                    "role": "tool",  # Rôle tool pour l'observation
                    "content": str(result),  # Résultat formaté en chaîne
                    "tool_call_id": tool_call.id  # Lie l'observation à l'appel
                })
    
    # Si on dépasse le nombre max d'étapes sans réponse finale
    return "Max steps atteint"
```

---

## 5. Système de prompt pour un agent

Voici un exemple de **system prompt** pour un agent complet :

```
Tu es un agent autonome capable d'utiliser des outils.
Règles :
1. Réfléchis avant d'agir (Thought: ...)
2. Utilise les outils à ta disposition si nécessaire (Action: ...)
3. Observe le résultat des outils (Observation: ...)
4. Réponds à l'utilisateur quand tu as assez d'informations

Outils disponibles :
- get_weather(ville) → météo actuelle
- search(query) → recherche web
- calculate(expression) → calcul mathématique

Ne JAMAIS inventer des résultats d'outils.
Si un outil échoue, explique pourquoi à l'utilisateur.
```

---

## 6. Travaux Pratiques — Assistant CLI avec Outils

> **Projet reseau social** : ce TP s'appuie sur le reseau social defini dans [`projet/gestion_de_projet/cdc.md`](projet/gestion_de_projet/cdc.md). L'assistant CLI que vous allez construire permettra de manipuler les utilisateurs et publications de cette application.

**Objectif :** Créer un assistant en ligne de commande qui utilise des outils (tool use) avec le pattern ReAct.

**Durée :** 2h

---

### 6.1 Énoncé

Vous devez creer un assistant interactif en ligne de commande avec :

1. Un outil **meteo** qui retourne la temperature d'une ville
2. Un outil **calcul** qui evalue une expression mathematique
3. Un systeme de **detection automatique** : l'assistant reconnait quelle action executer selon la question
4. Un fichier de configuration **opencode.json** pour ameliorer l'assistant avec un agent
5. Des **tests** pour chaque outil

**Fichiers à créer :**
- `assistant-cli/assistant.py` — l'assistant avec ses outils
- `assistant-cli/opencode.json` — configuration pour l'amelioration par agent
- `assistant-cli/AGENTS.md` — description de l'equipe
- `assistant-cli/.opencode/skills/common.md` — règles communes de l'agent
- `assistant-cli/test_assistant.py` — tests automatisés sans dépendance externe

---

### 6.2 Corrigé — Étape 1 : Structure du projet

```bash
mkdir assistant-cli && cd assistant-cli
```

Créez `assistant.py` :

```python
import json  # Pour la manipulation de données JSON
import sys   # Pour les interactions système (entrée/sortie)

class Assistant:
    def __init__(self):
        # Dictionnaire associant les noms d'outils à leurs implémentations
        self.tools = {
            "calculer": self.calculer,  # Outil de calcul mathématique
            "meteo": self.meteo,        # Outil de requête météo simulée
        }
    
    def calculer(self, expression: str) -> str:
        """Calcule une expression mathématique."""
        try:
            # eval évalue l'expression (attention : sécurité à vérifier)
            return str(eval(expression))
        except Exception as e:
            # Retourne un message d'erreur explicite
            return f"Erreur: {e}"
    
    def meteo(self, ville: str) -> str:
        """Simule une requête météo."""
        # Retourne une valeur fixe pour la simulation
        return f"15°C à {ville}, ciel nuageux"
    
    def run(self, question: str) -> str:
        # Version simplifiée du pattern ReAct
        # Analyse la question pour détecter une demande météo
        if "météo" in question.lower():
            # Parcourt une liste de villes prédéfinies
            for ville in ["Paris", "Lyon", "Marseille", "Tokyo", "Londres"]:
                if ville.lower() in question.lower():
                    # Appelle l'outil météo avec la ville trouvée
                    return self.meteo(ville)
        
        # Détecte les expressions mathématiques
        if "calcul" in question.lower() or "+" in question or "-" in question:
            # Extrait l'expression après le séparateur ":" si présent
            parts = question.split(":")[-1].strip() if ":" in question else question
            return self.calculer(parts)
        
        # Retourne un message par défaut si aucune correspondance
        return f"Je ne sais pas répondre à: {question}"

# Point d'entrée principal du programme
if __name__ == "__main__":
    agent = Assistant()  # Crée une instance de l'Assistant
    while True:          # Boucle interactive infinie
        q = input("\n> ")  # Attend la saisie de l'utilisateur
        if q == "quit":    # Commande pour quitter l'application
            break
        print(agent.run(q))  # Affiche la réponse de l'assistant
```

### 6.3 Corrigé — Étape 2 : Tester sans agent

```bash
python3 assistant.py
> météo à Paris
> calcul: 42 + 18
> quit
```

### 6.4 Corrigé — Étape 3 : Configurer opencode pour l'assistant

Créez les dossiers nécessaires :

```bash
mkdir -p .opencode/skills
```

Créez un fichier `opencode.json` à la racine du projet :

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/big-pickle",
  "default_agent": "developer",
  "instructions": ["AGENTS.md"],
  "skills": {"paths": [".opencode/skills"]},
  "agent": {
    "developer": {
      "mode": "primary",
      "description": "Développe l'assistant CLI",
      "skills": ["common"]
    }
  }
}
```

Créez `AGENTS.md` :

```markdown
# Assistant CLI avec outils

Ce projet contient un assistant en ligne de commande qui utilise deux outils :

- `meteo(ville)` : retourne une météo simulée
- `calculer(expression)` : calcule une expression mathématique simple

## Objectif

Améliorer progressivement l'assistant avec opencode : meilleure détection d'intention, nouveaux outils, tests.
```

Créez `.opencode/skills/common.md` :

```markdown
# Règles communes

Langage : Python 3.10+

Conventions :
- Code simple et lisible
- Commentaires pédagogiques
- Tests avec la bibliothèque standard `unittest`
- Ne pas ajouter de dépendance externe sans justification
```

### 6.5 Corrigé — Étape 4 : Ajouter les tests

Créez `test_assistant.py` :

```python
import unittest

from assistant import Assistant


class TestAssistant(unittest.TestCase):
    def setUp(self):
        # Crée un assistant neuf avant chaque test
        self.agent = Assistant()

    def test_meteo_paris(self):
        # Vérifie que l'outil météo répond pour Paris
        result = self.agent.run("météo à Paris")
        self.assertIn("15°C", result)
        self.assertIn("Paris", result)

    def test_calcul_simple(self):
        # Vérifie un calcul mathématique simple
        result = self.agent.run("calcul: 42 + 18")
        self.assertEqual(result, "60")

    def test_expression_invalide(self):
        # Vérifie qu'une expression invalide ne fait pas planter l'assistant
        result = self.agent.run("calcul: 42 +")
        self.assertIn("Erreur", result)

    def test_question_inconnue(self):
        # Vérifie que l'assistant répond même s'il ne sait pas traiter la demande
        result = self.agent.run("Bonjour")
        self.assertIn("Je ne sais pas", result)


if __name__ == "__main__":
    unittest.main()
```

Lancez les tests :

```bash
python3 -m unittest -v test_assistant.py
```

### 6.6 Corrigé — Étape 5 : Améliorer avec l'agent

Lancez opencode et demandez-lui d'améliorer l'assistant :

```
"Améliore l'assistant pour gérer la météo de n'importe quelle ville"
"Ajoute un outil de conversion euro → dollar"
"Ajoute des tests pour chaque outil"
```

### 6.7 Corrigé — Étape 6 : Validation

- [ ] L'assistant répond correctement aux questions météo
- [ ] L'assistant calcule des expressions mathématiques
- [ ] L'assistant gère les cas d'erreur (ville inconnue, expression invalide)
- [ ] `python3 -m unittest -v test_assistant.py` passe
- [ ] `opencode` charge bien `opencode.json` et `AGENTS.md`

### 6.8 Pour aller plus loin

- Implémentez le vrai pattern ReAct avec une boucle LLM
- Ajoutez un outil de recherche web (fichier local)
- Utilisez opencode pour ajouter une interface web Flask/FastAPI

---

## Points clés à retenir

1. Le **prompt engineering** est la première compétence à maîtriser pour interagir avec les LLMs
2. Le **few-shot** et le **chain-of-thought** améliorent significativement la qualité des réponses
3. Le **function calling** transforme un LLM passif en orchestrateur d'actions
4. Le **pattern ReAct** (Thought → Action → Observation) est la boucle fondamentale de tout système agentique
5. Un **system prompt bien conçu** est crucial pour le comportement d'un agent

---

## Liens

- [Chapitre 2 — Architecture des LLMs](./CHAPITRE-02-fondations-llm.md)
- [Chapitre 4 — Architecture Agentique](./CHAPITRE-04-architecture-agent.md)
- [Référence OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [ReAct Paper (Yao et al., 2023)](https://arxiv.org/abs/2210.03629)
