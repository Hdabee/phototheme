from PIL import Image, ImageEnhance, ImageOps
from app.editor.photo_state import PhotoEditState

def clamp(value: float, lower: float = 0.2, upper: float = 2.0) -> float:
    return max(lower, min(upper, float(value)))

def clamp_crop(value: float) -> float:
    return max(0.0, min(1.0, float(value)))

def apply_source_crop(image: Image.Image, state: PhotoEditState) -> Image.Image:
    x = clamp_crop(state.crop_x)
    y = clamp_crop(state.crop_y)
    width = max(0.02, min(1.0 - x, clamp_crop(state.crop_width)))
    height = max(0.02, min(1.0 - y, clamp_crop(state.crop_height)))
    left = round(image.width * x)
    top = round(image.height * y)
    right = max(left + 1, round(image.width * (x + width)))
    bottom = max(top + 1, round(image.height * (y + height)))
    return image.crop((left, top, right, bottom))

def transform_photo(image: Image.Image, state: PhotoEditState) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("RGB")
    image = apply_source_crop(image, state)
    rotation = int(state.rotation) % 360
    if rotation:
        image = image.rotate(-rotation, expand=True, resample=Image.Resampling.BICUBIC)
    if state.flip_horizontal:
        image = ImageOps.mirror(image)
    image = ImageEnhance.Brightness(image).enhance(clamp(state.brightness))
    image = ImageEnhance.Contrast(image).enhance(clamp(state.contrast))
    image = ImageEnhance.Color(image).enhance(clamp(state.saturation))
    image = ImageEnhance.Sharpness(image).enhance(clamp(state.sharpness))
    return image
