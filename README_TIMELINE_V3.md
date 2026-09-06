# PhotoTheme Web V3 — Découpage photo composée et frise d'évolution

## Installation

Placez `install_phototheme_web_v3_composite_timeline.py` dans le dossier parent de `phototheme-python-starter`, puis lancez :

```powershell
py .\install_phototheme_web_v3_composite_timeline.py
```

Démarrez ensuite l'application :

```powershell
cd .\phototheme-python-starter
.\start.ps1
```

Ouvrez `http://127.0.0.1:8000` puis faites `Ctrl + F5`.

## Cas d'usage : photo composée + photo récente

1. Importez la photo composée seule.
2. Cliquez sur sa vignette.
3. Cliquez sur `Découper en 3 portraits`.
4. Sélectionnez et éditez les trois vignettes créées.
5. Ajoutez ensuite une photo récente : pour cette V3 simple, recommencez une nouvelle session en important les 4 images ensemble, ou utilisez l'import simultané dès le départ si la photo récente est disponible.
6. Choisissez `Timeline Evolution` et `Heritage Timeline`.
7. Créez le PNG.

La V3 réalise une découpe égale en trois zones verticales. La prochaine itération ajoutera les poignées visuelles pour déplacer et redimensionner librement chaque zone.
