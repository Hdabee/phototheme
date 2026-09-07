from pathlib import Path

from PIL import Image

from app.editor.photo_state import PhotoEditState
from app.editor.photo_transformer import transform_photo
from app.renderer.image_ops import fit_contain, fit_cover
from app.renderer.render_context import RenderContext
from app.renderer.theme_renderer_factory import ThemeRendererFactory


def cover(image, width, height):
    """Compatibility alias retained for legacy callers and tests."""
    return fit_cover(image, width, height)


def contain(image, width, height, background_color):
    """Compatibility alias retained for legacy callers and tests."""
    return fit_contain(image, width, height, background_color)


def normalize_states(items):
    normalized = []
    for index, item in enumerate(items):
        normalized.append(item if isinstance(item, PhotoEditState) else PhotoEditState(photo_id=f"photo_{index}", source_path=str(item)))
    return normalized


def render_collage(states, layout, theme, output: Path, size: int = 1080, story=None):
    states = normalize_states(states)
    canvas = Image.new("RGBA", (size, size), theme.get("background", "#F2EFE8"))
    rendered = []
    for state in states:
        with Image.open(state.source_path) as raw:
            rendered.append((state.photo_id, transform_photo(raw, state), state.caption))

    if story is None:
        from app.editor.project_story import ProjectStoryState
        story = ProjectStoryState(hero_photo_id=states[-1].photo_id if states else "")

    context = RenderContext(
        canvas=canvas,
        states=states,
        rendered=rendered,
        layout=layout,
        theme=theme,
        story=story,
        size=size,
    )
    renderer = ThemeRendererFactory.create(theme)
    renderer(context)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG", optimize=True)
    return output
