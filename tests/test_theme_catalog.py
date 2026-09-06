import json
from pathlib import Path


def test_theme_catalog_contains_unique_ids_and_backgrounds():
    themes = json.loads(Path("app/catalog/themes.json").read_text(encoding="utf-8"))
    ids = [theme["id"] for theme in themes]
    backgrounds = [theme["background"] for theme in themes]

    assert len(themes) >= 4
    assert len(ids) == len(set(ids))
    assert len(backgrounds) == len(set(backgrounds))
    assert "portrait-timeline-editorial" in ids
