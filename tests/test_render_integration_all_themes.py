import json
from pathlib import Path

import pytest
from PIL import Image

from app.editor.photo_state import PhotoEditState
from app.editor.project_story import ProjectStoryState
from app.renderer.collage_renderer import render_collage

ROOT = Path(__file__).resolve().parents[1]
THEMES = json.loads((ROOT / "app" / "catalog" / "themes.json").read_text(encoding="utf-8"))
LAYOUTS = json.loads((ROOT / "app" / "catalog" / "layouts.json").read_text(encoding="utf-8"))


def compatible_layout(theme, count):
    for layout_id in theme.get("preferred_layouts", []):
        for layout in LAYOUTS:
            if layout["id"] == layout_id and layout["photo_count"] == count:
                return layout
    return next(layout for layout in LAYOUTS if layout["photo_count"] == count)


def make_states(tmp_path, count, image_size):
    result = []
    for index in range(count):
        source = tmp_path / f"photo_{index}.png"
        Image.new("RGB", image_size, (45 + index * 30, 90 + index * 15, 150)).save(source)
        result.append(PhotoEditState(
            photo_id=f"photo_{index}", source_path=str(source), caption=f"Image {index + 1}",
            rotation=(index % 4) * 90, fit_mode="cover"
        ))
    return result


@pytest.mark.parametrize("theme", THEMES, ids=lambda theme: theme["id"])
@pytest.mark.parametrize("image_size", [(900, 900), (1, 2500), (2500, 1), (17, 997), (997, 17)])
def test_every_catalog_theme_renders_a_real_png(tmp_path, theme, image_size):
    states = make_states(tmp_path, 4, image_size)
    output = tmp_path / f"{theme['id']}.png"
    render_collage(
        states, compatible_layout(theme, 4), theme, output, size=1080,
        story=ProjectStoryState(
            title="UN TITRE DE TEST SUFFISAMMENT LONG", subtitle="Sous-titre de test.",
            period="1964 — 2026", place="THEN / NOW", hero_photo_id="photo_3"
        )
    )
    assert output.exists()
    assert output.stat().st_size > 0
    assert Image.open(output).size == (1080, 1080)
