# Extension Web V1 — PhotoTheme

## Installation

1. Placez `install_phototheme_web_v1.py` dans le dossier parent de `phototheme-python-starter`.
2. Lancez :

```powershell
py .\install_phototheme_web_v1.py
```

3. Ouvrez `phototheme-python-starter` dans VS Code.
4. Lancez :

```powershell
.\start.ps1
```

Le script mettra à jour les dépendances et démarrera le serveur.

## Utilisation

Ouvrez `http://127.0.0.1:8000`.

- Importez entre 2 et 9 photos.
- Sélectionnez occasion, style et format.
- Cliquez sur `Recommander un style`.
- Cliquez sur `Créer mon collage PNG`.
- Téléchargez l'image.

## Tests

```powershell
.\test.ps1
```

Les collages générés sont stockés dans `data/outputs/`.
