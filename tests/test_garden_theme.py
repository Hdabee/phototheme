from PIL import Image

from app.editor.photo_state import PhotoEditState
from app.editor.project_story import ProjectStoryState
from app.renderer.art_direction.garden import render_garden


def make_photos(tmp_path, count):
    photos = []
    colors = ["#D9806B", "#61956D", "#D8B35B", "#4D7D9D"]
    for index in range(count):
        source = tmp_path / f"garden_{index}.png"
        Image.new("RGB", (37 if index % 2 else 1100, 1300 if index % 2 else 53), colors[index]).save(source)
        state = PhotoEditState(photo_id=f"photo_{index}", source_path=str(source), caption=["Façade", "Jardin", "Floraison", "Maison"][index])
        with Image.open(source) as image:
            photos.append((state.photo_id, image.copy(), state.caption))
    return photos


def test_garden_renders_four_photos_with_extreme_aspects(tmp_path):
    canvas = Image.new("RGBA", (1080, 1080), "#4C6A58")
    photos = make_photos(tmp_path, 4)
    render_garden(canvas, photos, ProjectStoryState(title="Jardin d'été", subtitle="Lumière et souvenirs", place="Un lieu · quatre regards", period="Été 2026", hero_photo_id="photo_3"))
    assert canvas.size == (1080, 1080)
    assert canvas.getbbox() is not None


def test_garden_renders_three_photos_without_an_empty_photo_failure(tmp_path):
    canvas = Image.new("RGBA", (1080, 1080), "#4C6A58")
    photos = make_photos(tmp_path, 3)
    render_garden(canvas, photos, ProjectStoryState(hero_photo_id="photo_2"))
    assert canvas.size == (1080, 1080)
    assert canvas.getbbox() is not None
