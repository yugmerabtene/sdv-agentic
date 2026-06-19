# Lab 6 — CI/CD (Continuous Integration / Continuous Deployment) pour Agents

**Objectif :** Mettre en place un pipeline CI/CD complet qui teste et valide des agents automatiquement.

**Durée :** 2h

---

## Étape 1 — Structure du projet

```bash
mkdir cicd-agents && cd cicd-agents
# Reprenez les fichiers du Lab 2 (assistant CLI)
cp -r ../assistant-cli/* .
```

## Étape 2 — Tests comportementaux

Créez `tests/test_agent_behavior.py` :

```python
import sys
sys.path.append("..")
from assistant import Assistant

def test_meteo_paris():
    agent = Assistant()
    result = agent.run("météo à Paris")
    assert "°C" in result or "degrés" in result

def test_meteo_tokyo():
    agent = Assistant()
    result = agent.run("météo à Tokyo")
    assert "°C" in result or "degrés" in result

def test_calcul_simple():
    agent = Assistant()
    result = agent.run("calcul: 2 + 2")
    assert "4" in result

def test_calcul_complexe():
    agent = Assistant()
    result = agent.run("calcul: (10 + 5) * 2")
    assert "30" in result

def test_question_inconnue():
    agent = Assistant()
    result = agent.run("quelle est la couleur du ciel ?")
    assert result  # Ne doit pas planter

def test_ville_inconnue():
    agent = Assistant()
    result = agent.run("météo à Inconnueville")
    assert result  # Ne doit pas planter
```

## Étape 3 — Tests de qualité

Créez `tests/test_quality.py` :

```python
import subprocess

def test_lint():
    result = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)
    assert result.returncode == 0, f"Lint erreurs:\n{result.stdout}"

def test_imports():
    result = subprocess.run(["python", "-c", "from assistant import Assistant"], 
                          capture_output=True, text=True)
    assert result.returncode == 0, f"Import échoué:\n{result.stderr}"
```

## Étape 4 — Pipeline GitHub Actions

Créez `.github/workflows/test-agents.yml` :

```yaml
name: Test Agents

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      
      - name: Installer les dépendances
        run: |
          python -m pip install --upgrade pip
          pip install pytest ruff
      
      - name: Qualité (ruff)
        run: ruff check .
      
      - name: Tests agents
        run: pytest tests/ -v
```

## Étape 5 — Tester en local

```bash
pip install pytest ruff
ruff check .
pytest tests/ -v
```

## Étape 6 — Configurer opencode pour le pipeline

Demandez à l'agent opencode :

```
"Ajoute un job 'benchmark' qui mesure le temps de réponse des outils"
"Ajoute un seuil d'échec : si un outil met plus de 2 secondes, le test échoue"
"Ajoute un rapport de couverture de code"
```

## Validation

- [ ] `pytest tests/` passe avec tous les tests verts
- [ ] `ruff check .` passe sans erreur
- [ ] Le pipeline GitHub Actions est configuré
- [ ] Les tests comportementaux valident les cas normaux ET les cas d'erreur

## Pour aller plus loin

- Ajoutez un benchmark qui mesure les tokens consommés par appel
- Créez un test de non-régression : exécutez l'agent sur 10 questions et stockez les réponses attendues
- Mettez en place un déploiement automatique si tous les tests passent
