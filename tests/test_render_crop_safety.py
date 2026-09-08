import pytest
from PIL import Image

from app.renderer.collage_renderer import cover
from app.renderer.image_ops import fit_contain, fit_cover
from app.renderer.art_direction.editorial_quality import fit_cover as editorial_fit_cover


CROP_FUNCTIONS = [cover, fit_cover, editorial_fit_cover]
IMAGE_SIZES = [
    (1, 1), (1, 2), (2, 1), (1, 5000), (5000, 1),
    (2, 3), (3, 2), (17, 997), (997, 17), (1080, 1080),
]
TARGET_SIZES = [
    (1, 1), (1, 2), (2, 1), (1, 1080), (1080, 1),
    (150, 455), (332, 530), (1080, 1080),
]


@pytest.mark.parametrize("cropper", CROP_FUNCTIONS)
@pytest.mark.parametrize("source_size", IMAGE_SIZES)
@pytest.mark.parametrize("target_size", TARGET_SIZES)
def test_cover_never_emits_invalid_crop_coordinates(cropper, source_size, target_size):
    image = Image.new("RGB", source_size, "#579BC5")
    result = cropper(image, *target_size)
    assert result.size == target_size


@pytest.mark.parametrize("cropper", CROP_FUNCTIONS)
def test_cover_clamps_zero_and_negative_target_dimensions(cropper):
    image = Image.new("RGB", (4, 7), "#579BC5")
    assert cropper(image, 0, 0).size == (1, 1)
    assert cropper(image, -30, 12).size == (1, 12)
    assert cropper(image, 12, -30).size == (12, 1)


@pytest.mark.parametrize("cropper", CROP_FUNCTIONS)
def test_cover_handles_rotated_extreme_aspect_images(cropper):
    for size in [(1, 3000), (3000, 1)]:
        image = Image.new("RGB", size, "#579BC5")
        for angle in (0, 90, 180, 270):
            rotated = image.rotate(angle, expand=True)
            output = cropper(rotated, 332, 530)
            assert output.size == (332, 530)


@pytest.mark.parametrize("source_size", IMAGE_SIZES)
@pytest.mark.parametrize("target_size", TARGET_SIZES)
def test_contain_never_emits_invalid_dimensions(source_size, target_size):
    image = Image.new("RGB", source_size, "#579BC5")
    result = fit_contain(image, *target_size, background_color="#F2EFE8")
    assert result.size == target_size


def test_contain_clamps_zero_and_negative_target_dimensions():
    image = Image.new("RGB", (4, 7), "#579BC5")
    assert fit_contain(image, 0, 0).size == (1, 1)
    assert fit_contain(image, -30, 12).size == (1, 12)
    assert fit_contain(image, 12, -30).size == (12, 1)
