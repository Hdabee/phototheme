from collections.abc import Mapping

from app.renderer.theme_renderer_registry import (
    RENDERER_REGISTRY,
    ThemeRenderer,
)


class UnknownThemeCompositionError(ValueError):
    """Raised when a theme has no known renderer composition."""


LEGACY_THEME_COMPOSITIONS = {
    "portrait-timeline-editorial": "portrait_timeline_editorial",
    "editorial-night": "portrait_timeline_night",
    "archive-vivante": "archive_story",
    "island-poster": "tropical_poster",
    "jardin-ete": "garden_poster",
    "chronique-de-vie": "life_chronicle",

    # Legacy generic themes still used by existing renderer tests.
    "editorial-magazine": "archive_story",
    "scrapbook-authentique": "archive_story",
    "contact-sheet-archive": "archive_story",
    "retro-sunshine": "archive_story",
    "minimal-gallery": "archive_story",
}


class ThemeRendererFactory:
    @staticmethod
    def composition_for(theme: Mapping[str, object]) -> str:
        composition = str(theme.get("composition") or "").strip()
        if composition:
            return composition

        theme_id = str(theme.get("id") or "").strip()
        if theme_id in LEGACY_THEME_COMPOSITIONS:
            return LEGACY_THEME_COMPOSITIONS[theme_id]

        raise UnknownThemeCompositionError(
            f"Theme sans composition connue : {theme_id!r}"
        )

    @staticmethod
    def create(theme_or_composition: Mapping[str, object] | str) -> ThemeRenderer:
        if isinstance(theme_or_composition, str):
            composition = theme_or_composition.strip()
        else:
            composition = ThemeRendererFactory.composition_for(theme_or_composition)

        try:
            return RENDERER_REGISTRY[composition]
        except KeyError as error:
            available = ", ".join(sorted(RENDERER_REGISTRY))
            raise UnknownThemeCompositionError(
                f"Composition de theme inconnue : {composition!r}. "
                f"Compositions disponibles : {available}"
            ) from error