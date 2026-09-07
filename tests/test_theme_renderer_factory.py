import pytest

from app.renderer.theme_renderer_factory import (
    ThemeRendererFactory,
    UnknownThemeCompositionError,
)
from app.renderer.theme_renderer_registry import RENDERER_REGISTRY


def test_factory_resolves_every_registered_composition():
    for composition in RENDERER_REGISTRY:
        assert callable(ThemeRendererFactory.create(composition))


def test_factory_rejects_an_unknown_composition_with_a_clear_error():
    with pytest.raises(UnknownThemeCompositionError, match="Composition de theme inconnue"):
        ThemeRendererFactory.create("not-a-real-composition")

def test_factory_resolves_a_legacy_theme_without_composition():
    renderer = ThemeRendererFactory.create(
        {"id": "editorial-magazine"}
    )
    assert callable(renderer)

def test_factory_resolves_minimal_gallery_without_composition():
    renderer = ThemeRendererFactory.create({"id": "minimal-gallery"})
    assert callable(renderer)
