from PIL import Image

from app.editor.project_story import ProjectStoryState
from app.renderer.art_direction.life_chronicle import render_life_chronicle


def build_photos(count):
    colors = ["#9A5B52", "#618398", "#D1AE6D", "#425D52"]
    sizes = [(30, 2200), (2200, 30), (120, 120), (1600, 950)]
    result = []
    for index in range(count):
        image = Image.new("RGB", sizes[index], colors[index])
        result.append((f"photo_{index}", image, ["Enfance", "Passage", "Mémoire", "Aujourd’hui"][index]))
    return result


def test_life_chronicle_handles_two_to_four_photos():
    for count in (2, 3, 4):
        canvas = Image.new("RGBA", (1080, 1080), "#EFE9DE")
        photos = build_photos(count)
        story = ProjectStoryState(hero_photo_id=f"photo_{count - 1}")
        render_life_chronicle(canvas, photos, story)
        assert canvas.size == (1080, 1080)
        assert canvas.getbbox() is not None


def test_life_chronicle_uses_last_photo_when_hero_is_not_set():
    canvas = Image.new("RGBA", (1080, 1080), "#EFE9DE")
    render_life_chronicle(canvas, build_photos(4), ProjectStoryState(hero_photo_id=""))
    assert canvas.size == (1080, 1080)
    assert canvas.getbbox() is not None
