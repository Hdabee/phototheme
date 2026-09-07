from PIL import Image


def _positive_dimension(value: int | float) -> int:
    return max(1, int(value))


def fit_cover(image: Image.Image | None, width: int | float, height: int | float, fill: str = "#D9D2C6") -> Image.Image:
    """Resize an image to fill the target box without invalid crop coordinates."""
    width, height = _positive_dimension(width), _positive_dimension(height)
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


def fit_contain(image: Image.Image | None, width: int | float, height: int | float, background_color: str = "#D9D2C6") -> Image.Image:
    """Resize an image inside the target box, preserving the full image on a background."""
    width, height = _positive_dimension(width), _positive_dimension(height)
    result = Image.new("RGB", (width, height), background_color)
    if image is None or image.width < 1 or image.height < 1:
        return result

    source = image.convert("RGB")
    ratio = source.width / source.height
    target_ratio = width / height
    if ratio > target_ratio:
        new_width, new_height = width, max(1, round(width / ratio))
    else:
        new_width, new_height = max(1, round(height * ratio)), height

    source = source.resize((new_width, new_height), Image.Resampling.LANCZOS)
    result.paste(source, ((width - new_width) // 2, (height - new_height) // 2))
    return result
