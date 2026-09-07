import json
from pathlib import Path

from app.renderer.theme_renderer_registry import RENDERER_REGISTRY


ROOT = Path(__file__).resolve().parents[1]
THEMES_PATH = ROOT / "app" / "catalog" / "themes.json"


def test_every_catalog_theme_declares_a_registered_composition():
    themes = json.loads(THEMES_PATH.read_text(encoding="utf-8"))
    for theme in themes:
        composition = theme.get("composition")
        assert composition, f"Theme sans composition : {theme.get('id', '<sans id>')}"
        assert composition in RENDERER_REGISTRY, (
            f"Composition non enregistree pour {theme.get('id', '<sans id>')}: {composition}"
        )
