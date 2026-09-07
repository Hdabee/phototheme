import pytest
from PIL import Image, ImageDraw

from app.renderer.art_direction.shapes import (
    safe_box,
    safe_ellipse,
    safe_rectangle,
    safe_rounded_rectangle,
    safe_line,
)


@pytest.mark.parametrize("box", [
    (0, 0, 10, 10),
    (10, 10, 0, 0),
    (10, 0, 0, 10),
    (0, 10, 10, 0),
    (-15, 8, 4, -9),
])
def test_safe_box_never_returns_inverted_coordinates(box):
    x0, y0, x1, y1 = safe_box(*box)
    assert x1 >= x0
    assert y1 >= y0


@pytest.mark.parametrize("drawer", [safe_ellipse, safe_rectangle])
@pytest.mark.parametrize("box", [
    (90, 70, 10, 5),
    (10, 60, 90, 2),
    (40, 40, 40, 40),
    (-30, 100, 50, -10),
])
def test_safe_primitives_accept_inverted_boxes(drawer, box):
    image = Image.new("RGBA", (120, 80), "#F2EFE8")
    drawer(ImageDraw.Draw(image), box, fill="#C45E3D")
    assert image.size == (120, 80)


@pytest.mark.parametrize("radius", [-10, 0, 3, 1000])
def test_safe_rounded_rectangle_clamps_radius(radius):
    image = Image.new("RGBA", (120, 80), "#F2EFE8")
    safe_rounded_rectangle(ImageDraw.Draw(image), (90, 70, 10, 5), radius=radius, fill="#C45E3D")
    assert image.size == (120, 80)


@pytest.mark.parametrize("segment", [
    (0, 0, 10, 10),
    (90, 70, 10, 5),
    (-30, 100, 50, -10),
    (4.4, 8.6, 80.2, 3.1),
])
def test_safe_line_accepts_diagonal_and_inverted_endpoints(segment):
    image = Image.new("RGBA", (120, 120), "#F2EFE8")
    safe_line(ImageDraw.Draw(image), segment, fill="#C45E3D", width=2)
    assert image.size == (120, 120)


def test_safe_line_rejects_an_invalid_coordinate_count():
    image = Image.new("RGBA", (120, 120), "#F2EFE8")
    with pytest.raises(ValueError, match="quatre coordonnees"):
        safe_line(ImageDraw.Draw(image), (1, 2, 3), fill="#C45E3D")
