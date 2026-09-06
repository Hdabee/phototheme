import json
from pathlib import Path


def test_art_direction_themes_have_unique_compositions():
    themes = json.loads(Path("app/catalog/themes.json").read_text(encoding="utf-8"))
    ids = {theme["id"] for theme in themes}
    compositions = [theme["composition"] for theme in themes]

    assert len(themes) >= 4
    assert len(compositions) == len(set(compositions))
    assert {"portrait-timeline-editorial", "editorial-night"}.issubset(ids)
