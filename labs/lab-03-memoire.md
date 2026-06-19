# Lab 3 — Agent avec Mémoire Persistante

**Objectif :** Ajouter de la mémoire long-terme à un agent en utilisant SQLite.

**Durée :** 2h

---

## Étape 1 — Structure

```bash
mkdir agent-memoire && cd agent-memoire
```

## Étape 2 — Agent avec mémoire

Créez `agent_memoire.py` :

```python
import sqlite3
import json
from datetime import datetime

class AgentMemoire:
    def __init__(self, db_path="memoire.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()
    
    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memoire (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cle TEXT UNIQUE,
                valeur TEXT,
                date_maj TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS historique (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                reponse TEXT,
                date TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def retenir(self, cle: str, valeur: str):
        self.conn.execute(
            "INSERT OR REPLACE INTO memoire (cle, valeur, date_maj) VALUES (?, ?, ?)",
            (cle, valeur, datetime.now())
        )
        self.conn.commit()
    
    def rappeler(self, cle: str) -> str | None:
        cursor = self.conn.execute(
            "SELECT valeur FROM memoire WHERE cle = ?", (cle,)
        )
        row = cursor.fetchone()
        return row[0] if row else None
    
    def toutes_cles(self) -> list[str]:
        cursor = self.conn.execute("SELECT cle FROM memoire")
        return [row[0] for row in cursor.fetchall()]
    
    def run(self, question: str) -> str:
        # Stocke la question
        self.conn.execute(
            "INSERT INTO historique (question, date) VALUES (?, ?)",
            (question, datetime.now())
        )
        self.conn.commit()
        
        # Commandes de mémoire
        if question.startswith("souviens-toi que "):
            contenu = question.replace("souviens-toi que ", "")
            if " est " in contenu:
                cle, valeur = contenu.split(" est ", 1)
                self.retenir(cle.strip(), valeur.strip())
                return f"J'ai retenu que {cle} est {valeur}"
        
        if question.startswith("que sais-tu sur "):
            sujet = question.replace("que sais-tu sur ", "")
            valeur = self.rappeler(sujet.strip())
            if valeur:
                return f"Je sais que {sujet} est {valeur}"
            return f"Je ne sais rien sur {sujet}"
        
        if question == "liste ce que tu sais":
            cles = self.toutes_cles()
            if cles:
                return "Je connais: " + ", ".join(cles)
            return "Je ne connais rien pour l'instant"
        
        return f"Question reçue: {question}"

if __name__ == "__main__":
    agent = AgentMemoire()
    while True:
        q = input("\n> ")
        if q == "quit":
            break
        print(agent.run(q))
```

## Étape 3 — Tester

```bash
python agent_memoire.py
> souviens-toi que Paris est la capitale de la France
> que sais-tu sur Paris
> liste ce que tu sais
> quit
```

Vérifiez que les données persistent :

```bash
python agent_memoire.py
> que sais-tu sur Paris   # Doit encore répondre !
```

## Étape 4 — Configurer opencode

Créez `opencode.json` et `AGENTS.md` (cf. Lab 1). Lancez opencode et demandez :

```
"Ajoute une commande 'oublie tout' qui vide la mémoire"
"Ajoute un compteur de questions posées"
"Crée un test qui vérifie la persistance des données"
```

## Validation

- [ ] L'agent retient les informations entre les sessions
- [ ] L'agent peut lister ce qu'il connaît
- [ ] Les données persistent après redémarrage (vérifiez avec SQLite)
- [ ] Les tests passent

## Aller plus loin — Version vectorielle

Pour une vraie mémoire sémantique, utilisez des embeddings :

```bash
pip install chromadb sentence-transformers
```

Et remplacez SQLite par Chroma pour la recherche par similarité.

## Pour aller plus loin

- Ajoutez une date d'expiration aux souvenirs
- Implémentez un "résumé automatique" des longues conversations
- Utilisez opencode avec l'agent développeur pour ajouter une API (Application Programming Interface) REST
