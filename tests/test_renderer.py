from pathlib import Path
from PIL import Image
from app.editor.photo_state import PhotoEditState
from app.renderer.collage_renderer import render_collage


def test_render_quad(tmp_path):
    states = []
    for index, color in enumerate(["red", "green", "blue", "yellow"]):
        path = tmp_path / f"{index}.png"
        Image.new("RGB", (400, 300), color).save(path)
        states.append(PhotoEditState(photo_id=f"photo_{index}", source_path=str(path)))

    output = tmp_path / "out.png"
    layout = {"id": "quad-classic", "photo_count": 4}
    theme = {"id": "minimal-gallery", "background": "#F8F3EA", "premium": False}
    render_collage(states, layout, theme, output, size=360)

    assert output.exists()
    assert Image.open(output).size == (360, 360)
