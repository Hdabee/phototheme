# PhotoTheme Factory — Python Local Mock Starter

## Objectif

Prototype local du backend agentique PhotoTheme. Il ne nécessite aucune clé API, aucun modèle LLM externe, aucune base cloud et aucun compte utilisateur.

Le projet simule une architecture factory avec :

- un orchestrateur ;
- une `SkillAgentFactory` ;
- un registre d'agents ;
- un agent de recommandation de layouts ;
- un agent de recommandation de thèmes ;
- un agent QA ;
- des guardrails d'entrée, de sortie et de budget ;
- un système de traces JSONL ;
- des tests pytest et scénarios d'évaluation de dérive.

## Démarrage rapide Windows / VS Code

1. Décompressez l'archive.
2. Ouvrez le dossier dans VS Code.
3. Dans un terminal PowerShell :

```powershell
.\start.ps1
```

Le script crée `.venv`, installe les dépendances et lance l'API sur `http://127.0.0.1:8000`.

Ouvrez ensuite `http://127.0.0.1:8000/docs` dans votre navigateur.

## Tests

Dans un second terminal :

```powershell
.\test.ps1
```

Ou lancez les évaluations :

```powershell
.\.venv\Scripts\python.exe evals\run_evals.py
```

## Endpoints

- `GET /api/v1/health`
- `GET /api/v1/catalog/themes`
- `GET /api/v1/catalog/layouts`
- `POST /api/v1/recommend-layout`
- `POST /api/v1/recommend-theme`
- `POST /api/v1/workflow`

## Exemple de requête

```json
{
  "photo_count": 4,
  "target_format": "square",
  "occasion": "anniversaire",
  "style_hint": "pastel",
  "locale": "fr-FR"
}
```

## VS Code

Installez les extensions Python et Pylance. Sélectionnez ensuite l'interpréteur `.venv\Scripts\python.exe`. Utilisez F5 et choisissez `PhotoTheme API (FastAPI)` pour debugger.

## Passage ultérieur à un LLM réel

Le code mock est volontairement séparé dans les agents. Pour ajouter un fournisseur LLM plus tard, conservez l'interface `SkillAgent`, puis remplacez l'implémentation de chaque agent ou ajoutez un adaptateur de modèle derrière la factory. Conservez les guardrails, les budgets et les tests d'évaluation existants.
