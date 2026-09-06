import json
from pathlib import Path

class CatalogService:
    def __init__(self):
        catalog_path = Path(__file__).resolve().parents[1] / "catalog"
        self.themes = json.loads((catalog_path / "themes.json").read_text(encoding="utf-8"))
        self.layouts = json.loads((catalog_path / "layouts.json").read_text(encoding="utf-8"))
