from pathlib import Path
from PIL import Image
from app.editor.photo_state import PhotoEditState
from app.editor.photo_transformer import transform_photo
from app.renderer.render_context import RenderContext
from app.renderer.theme_renderer_factory import ThemeRendererFactory



from PIL import Image


def safe_cover(image, width, height, fill="#D9D2C6"):
    width = max(1, int(width))
    height = max(1, int(height))

    if image is None or image.width < 1 or image.height < 1:
        return Image.new("RGB", (width, height), fill)

    source = image.convert("RGB")
    source_ratio = source.width / source.height
    target_ratio = width / height

    if source_ratio >= target_ratio:
        resized_height = height
        resized_width = max(width, round(height * source_ratio))
    else:
        resized_width = width
        resized_height = max(height, round(width / source_ratio))

    source = source.resize(
        (max(1, resized_width), max(1, resized_height)),
        Image.Resampling.LANCZOS,
    )

    left = max(0, (source.width - width) // 2)
    top = max(0, (source.height - height) // 2)
    right = min(source.width, left + width)
    bottom = min(source.height, top + height)

    if right <= left or bottom <= top:
        return Image.new("RGB", (width, height), fill)

    cropped = source.crop((left, top, right, bottom))

    if cropped.size == (width, height):
        return cropped

    result = Image.new("RGB", (width, height), fill)
    result.paste(
        cropped,
        (
            max(0, (width - cropped.width) // 2),
            max(0, (height - cropped.height) // 2),
        ),
    )
    return result


def safe_cover(image, width, height, fill="#D9D2C6"):
    width = max(1, int(width))
    height = max(1, int(height))
    if image is None or image.width < 1 or image.height < 1:
        return Image.new("RGB", (width, height), fill)

    source = image.convert("RGB")
    source_ratio = source.width / source.height
    target_ratio = width / height
    if source_ratio >= target_ratio:
        resized_width = max(width, round(height * source_ratio))
        resized_height = height
    else:
        resized_width = width
        resized_height = max(height, round(width / source_ratio))

    source = source.resize((max(1, resized_width), max(1, resized_height)), Image.Resampling.LANCZOS)
    left = max(0, (source.width - width) // 2)
    top = max(0, (source.height - height) // 2)
    right = min(source.width, left + width)
    bottom = min(source.height, top + height)

    if right <= left or bottom <= top:
        return Image.new("RGB", (width, height), fill)

    cropped = source.crop((left, top, right, bottom))
    if cropped.size == (width, height):
        return cropped

    result = Image.new("RGB", (width, height), fill)
    result.paste(cropped, ((width - cropped.width) // 2, (height - cropped.height) // 2))
    return result


def cover(image, width, height):
    return safe_cover(image, width, height)

def contain(image, width, height, background_color):
    ratio = image.width / image.height
    target = width / height
    new_width, new_height = (width, round(width / ratio)) if ratio > target else (round(height * ratio), height)
    result = Image.new("RGB", (width, height), background_color)
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    result.paste(image, ((width - new_width) // 2, (height - new_height) // 2))
    return result


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
