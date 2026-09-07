from pathlib import Path
from PIL import Image
from app.editor.photo_state import PhotoEditState
from app.editor.photo_transformer import transform_photo
from app.renderer.layout_geometry import cells_for
from app.renderer.art_direction.atelier import render_atelier
from app.renderer.art_direction.garden import render_garden
from app.renderer.art_direction.life_chronicle import render_life_chronicle
from app.renderer.art_direction.editorial_quality import render_editorial_night, render_portrait_timeline_editorial
from app.renderer.art_direction.themes import background, overlays, stylize



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
    theme_id = theme.get("id", "portrait-timeline-editorial")
    canvas = Image.new("RGBA", (size, size), theme.get("background", "#F2EFE8"))
    rendered = []
    for state in states:
        with Image.open(state.source_path) as raw:
            rendered.append((state.photo_id, transform_photo(raw, state), state.caption))

    if story is None:
        from app.editor.project_story import ProjectStoryState
        story = ProjectStoryState(hero_photo_id=states[-1].photo_id if states else "")

    if theme_id == "portrait-timeline-editorial":
        render_portrait_timeline_editorial(canvas, rendered, story)
    elif theme_id == "editorial-night":
        render_editorial_night(canvas, rendered, story)
    elif theme_id in {"reconstructed-portrait", "island-poster"}:
        render_atelier(canvas, theme_id, rendered, story)
    elif theme_id == "jardin-ete":
        render_garden(canvas, rendered, story)
    elif theme_id == "chronique-de-vie":
        render_life_chronicle(canvas, rendered, story)
    else:
        background(canvas, theme_id)
        cells = cells_for(layout["id"], size, 16)
        for index, (state, cell) in enumerate(zip(states, cells)):
            x, y, width, height = cell
            photo = stylize(rendered[index][1], theme_id)
            photo = cover(photo, width, height) if state.fit_mode == "cover" else contain(photo, width, height, theme.get("background", "#F2EFE8"))
            frame = Image.new("RGBA", (width + 20, height + 20), "#FFFEFA")
            frame.paste(photo.convert("RGBA"), (10, 10))
            canvas.alpha_composite(frame, (x - 10, y - 10))
        overlays(canvas, theme_id, states, cells)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, "PNG", optimize=True)
    return output
