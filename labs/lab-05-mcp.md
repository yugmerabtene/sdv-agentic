# Lab 5 — Serveur MCP (Model Context Protocol)

**Objectif :** Créer un serveur MCP (Model Context Protocol) et le connecter à opencode.

**Durée :** 2h

---

## Étape 1 — Installer le SDK MCP

```bash
mkdir serveur-mcp && cd serveur-mcp
pip install mcp
```

## Étape 2 — Serveur MCP minimal

Créez `serveur_meteo.py` :

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("meteo-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description="Obtenir la météo d'une ville",
            parameters={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Nom de la ville"
                    }
                },
                "required": ["city"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, args: dict) -> list[TextContent]:
    if name == "get_weather":
        # Simulation météo
        temperatures = {
            "paris": "15°C, ciel nuageux",
            "tokyo": "22°C, ensoleillé",
            "londres": "12°C, pluie légère",
            "new york": "18°C, vent modéré",
        }
        city = args["city"].lower()
        result = temperatures.get(city, f"20°C à {args['city']}, données approximatives")
        return [TextContent(result)]
    
    raise ValueError(f"Outil inconnu: {name}")

if __name__ == "__main__":
    app.run(transport="stdio")
```

## Étape 3 — Tester le serveur

```bash
python serveur_meteo.py
# Le serveur écoute sur stdio (utilisable par un client MCP)
```

## Étape 4 — Client MCP

Créez `client_test.py` :

```python
import asyncio
import json
from mcp.client import Client

async def test():
    async with Client.connect("python serveur_meteo.py") as client:
        tools = await client.list_tools()
        print("Outils disponibles:", [t.name for t in tools])
        
        result = await client.call_tool("get_weather", {"city": "Paris"})
        print("Résultat:", result)

asyncio.run(test())
```

## Étape 5 — Connecter à opencode

Ajoutez dans `opencode.json` :

```json
{
  "mcp_servers": {
    "meteo": {
      "command": "python",
      "args": ["serveur_meteo.py"]
    }
  },
  "agent": {
    "assistant": {
      "mode": "primary",
      "description": "Assistant avec accès météo",
      "mcp_servers": ["meteo"]
    }
  }
}
```

## Étape 6 — Tester avec opencode

Lancez opencode et demandez :

```
"Quel temps fait-il à Tokyo ?"
"Et à Paris ?"
"Quelle est la différence de température entre Londres et New York ?"
```

## Validation

- [ ] Le serveur MCP répond aux requêtes
- [ ] Le client MCP se connecte et appelle les outils
- [ ] opencode utilise le serveur MCP pour répondre aux questions météo
- [ ] L'agent opencode combine les appels MCP (ex: comparer deux villes)

## Pour aller plus loin

- Ajoutez un outil `get_time(city)` qui retourne l'heure locale
- Créez un serveur MCP pour votre base de données (ex: SQLite)
- Hébergez le serveur MCP via HTTP au lieu de stdio
