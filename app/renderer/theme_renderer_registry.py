from collections.abc import Callable

from PIL import Image

from app.renderer.art_direction.atelier import render_atelier
from app.renderer.art_direction.editorial_quality import (
    render_editorial_night,
    render_portrait_timeline_editorial,
)
from app.renderer.art_direction.garden import render_garden
from app.renderer.art_direction.life_chronicle import render_life_chronicle
from app.renderer.art_direction.themes import background, overlays, stylize
from app.renderer.layout_geometry import cells_for
from app.renderer.render_context import RenderContext

ThemeRenderer = Callable[[RenderContext], None]


def _safe_cover(image: Image.Image, width: int, height: int, fill: str = "#D9D2C6") -> Image.Image:
    width, height = max(1, int(width)), max(1, int(height))
    if image is None or image.width < 1 or image.height < 1:
        return Image.new("RGB", (width, height), fill)

    source = image.convert("RGB")
    source_ratio = source.width / source.height
    target_ratio = width / height
    if source_ratio >= target_ratio:
        resized_width, resized_height = max(width, round(height * source_ratio)), height
    else:
        resized_width, resized_height = width, max(height, round(width / source_ratio))

    source = source.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
    left = max(0, (source.width - width) // 2)
    top = max(0, (source.height - height) // 2)
    return source.crop((left, top, left + width, top + height))


def _contain(image: Image.Image, width: int, height: int, background_color: str) -> Image.Image:
    width, height = max(1, int(width)), max(1, int(height))
    source = image.convert("RGB")
    ratio = source.width / source.height
    target = width / height
    new_width, new_height = (
        (width, max(1, round(width / ratio)))
        if ratio > target
        else (max(1, round(height * ratio)), height)
    )
    result = Image.new("RGB", (width, height), background_color)
    source = source.resize((new_width, new_height), Image.Resampling.LANCZOS)
    result.paste(source, ((width - new_width) // 2, (height - new_height) // 2))
    return result


def render_portrait_timeline(context: RenderContext) -> None:
    render_portrait_timeline_editorial(context.canvas, context.rendered, context.story)


def render_night_timeline(context: RenderContext) -> None:
    render_editorial_night(context.canvas, context.rendered, context.story)


def render_tropical_poster(context: RenderContext) -> None:
    render_atelier(context.canvas, "island-poster", context.rendered, context.story)


def render_garden_poster(context: RenderContext) -> None:
    render_garden(context.canvas, context.rendered, context.story)


def render_life_story(context: RenderContext) -> None:
    render_life_chronicle(context.canvas, context.rendered, context.story)


def render_generic_catalog(context: RenderContext) -> None:
    theme_id = context.theme.get("id", "")
    background(context.canvas, theme_id)
    cells = cells_for(context.layout["id"], context.size, 16)
    for state, rendered_photo, cell in zip(context.states, context.rendered, cells):
        x, y, width, height = cell
        photo = stylize(rendered_photo[1], theme_id)
        photo = (
            _safe_cover(photo, width, height)
            if state.fit_mode == "cover"
            else _contain(photo, width, height, context.theme.get("background", "#F2EFE8"))
        )
        frame = Image.new("RGBA", (width + 20, height + 20), "#FFFEFA")
        frame.paste(photo.convert("RGBA"), (10, 10))
        context.canvas.alpha_composite(frame, (x - 10, y - 10))
    overlays(context.canvas, theme_id, context.states, cells)


RENDERER_REGISTRY: dict[str, ThemeRenderer] = {
    "portrait_timeline_editorial": render_portrait_timeline,
    "portrait_timeline_night": render_night_timeline,
    "archive_story": render_generic_catalog,
    "tropical_poster": render_tropical_poster,
    "garden_poster": render_garden_poster,
    "life_chronicle": render_life_story,
}
