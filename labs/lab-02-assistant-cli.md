# Lab 2 — Assistant CLI avec Outils

**Objectif :** Créer un assistant en ligne de commande qui utilise des outils (tool use) avec le pattern ReAct (Reasoning + Acting).

**Durée :** 2h

---

## Étape 1 — Structure du projet

```bash
mkdir assistant-cli && cd assistant-cli
```

Créez `assistant.py` :

```python
import json
import sys

class Assistant:
    def __init__(self):
        self.tools = {
            "calculer": self.calculer,
            "meteo": self.meteo,
        }
    
    def calculer(self, expression: str) -> str:
        """Calcule une expression mathématique."""
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Erreur: {e}"
    
    def meteo(self, ville: str) -> str:
        """Simule une requête météo."""
        return f"15°C à {ville}, ciel nuageux"
    
    def run(self, question: str) -> str:
        # Version simplifiée du pattern ReAct
        if "météo" in question.lower():
            for ville in ["Paris", "Lyon", "Marseille", "Tokyo", "Londres"]:
                if ville.lower() in question.lower():
                    return self.meteo(ville)
        
        if "calcul" in question.lower() or "+" in question or "-" in question:
            # Extraire l'expression
            parts = question.split(":")[-1].strip() if ":" in question else question
            return self.calculer(parts)
        
        return f"Je ne sais pas répondre à: {question}"

if __name__ == "__main__":
    agent = Assistant()
    while True:
        q = input("\n> ")
        if q == "quit":
            break
        print(agent.run(q))
```

## Étape 2 — Tester sans agents

```bash
python assistant.py
> météo à Paris
> calcul: 42 + 18
> quit
```

## Étape 3 — Configurer opencode

`opencode.json` :

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

## Étape 4 — Demander à l'agent

Lancez opencode et demandez :

```
"Améliore l'assistant pour gérer la météo de n'importe quelle ville"
"Ajoute un outil de conversion euro → dollar"
"Ajoute des tests pour chaque outil"
```

## Validation

- [ ] L'assistant répond correctement aux questions météo
- [ ] L'assistant calcule des expressions mathématiques
- [ ] L'assistant gère les cas d'erreur (ville inconnue, expression invalide)
- [ ] Les tests passent

## Pour aller plus loin

- Implémentez le vrai pattern ReAct avec une boucle LLM (Large Language Model)
- Ajoutez un outil de recherche web (fichier local)
- Utilisez opencode pour ajouter une interface web Flask/FastAPI
