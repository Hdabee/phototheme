import pytest
from PIL import Image

from app.renderer.image_ops import fit_contain, fit_cover


@pytest.mark.parametrize("operation", [fit_cover, fit_contain])
@pytest.mark.parametrize("source_size", [(1, 1), (1, 5000), (5000, 1), (17, 997), (997, 17)])
@pytest.mark.parametrize("target_size", [(1, 1), (1, 1080), (1080, 1), (332, 530), (1080, 1080)])
def test_image_ops_produce_the_requested_size(operation, source_size, target_size):
    image = Image.new("RGB", source_size, "#579BC5")
    assert operation(image, *target_size).size == target_size


@pytest.mark.parametrize("operation", [fit_cover, fit_contain])
def test_image_ops_clamp_invalid_target_dimensions(operation):
    image = Image.new("RGB", (4, 7), "#579BC5")
    assert operation(image, 0, 0).size == (1, 1)
    assert operation(image, -20, 9).size == (1, 9)
    assert operation(image, 9, -20).size == (9, 1)


@pytest.mark.parametrize("operation", [fit_cover, fit_contain])
def test_image_ops_accept_none_images(operation):
    assert operation(None, 24, 36).size == (24, 36)
