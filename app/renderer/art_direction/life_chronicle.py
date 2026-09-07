from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from app.renderer.art_direction.shapes import (
    safe_ellipse,
    safe_rectangle,
    safe_polygon,
)
from app.renderer.image_ops import fit_cover

PAPER = (239, 233, 222, 255)
INK = (39, 37, 33, 255)
MUTED = (105, 94, 79, 255)
ACCENT = (181, 88, 58, 255)
ACCENT_SOFT = (214, 183, 157, 255)
FRAME = (255, 252, 245, 255)


def load_font(size, bold=False, serif=False):
    candidates = []
    if serif:
        candidates.append("C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf")
    else:
        candidates.extend([
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        ])
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def archive_treatment(image):
    image = ImageEnhance.Color(image.convert("RGB")).enhance(0.58)
    image = ImageEnhance.Contrast(image).enhance(0.95)
    return Image.blend(image, Image.new("RGB", image.size, "#D4B892"), 0.10)


def present_treatment(image):
    image = ImageEnhance.Contrast(image.convert("RGB")).enhance(1.05)
    return ImageEnhance.Color(image).enhance(0.96)


def text_width(draw, text, used_font):
    box = draw.textbbox((0, 0), text, font=used_font)
    return box[2] - box[0]


def draw_title(draw, title, x, y, max_width):
    title = str(title or "CHRONIQUE DE VIE").upper()
    for size in (48, 44, 40, 36, 32):
        used_font = load_font(size, bold=True, serif=True)
        if text_width(draw, title, used_font) <= max_width:
            draw.text((x, y), title, font=used_font, fill=INK)
            return
    draw.text((x, y), title[:42], font=load_font(32, bold=True, serif=True), fill=INK)


def framed_photo(canvas, image, x, y, width, height, border=7, archive=False):
    treated = archive_treatment(image) if archive else present_treatment(image)
    photo = fit_cover(treated, width, height)
    frame = Image.new("RGBA", (width + 2 * border, height + 2 * border), FRAME)
    frame.paste(photo.convert("RGBA"), (border, border))
    canvas.alpha_composite(frame, (x - border, y - border))


def label(draw, number, caption, x, y, small=False):
    draw.text((x, y), number, font=load_font(14 if not small else 11, bold=True), fill=ACCENT)
    draw.text((x + (31 if not small else 24), y), caption.upper(), font=load_font(12 if not small else 10, bold=True), fill=INK)


def render_life_chronicle(canvas, photos, story):
    width, height = canvas.size
    draw = ImageDraw.Draw(canvas, "RGBA")
    safe_rectangle(draw, (0, 0, width, height), fill=PAPER)

    margin = 56
    draw_title(draw, getattr(story, "title", ""), margin, 54, width - 300)
    draw.text((margin, 117), str(getattr(story, "subtitle", "") or "Quatre moments, un même récit"), font=load_font(17), fill=MUTED)
    period = str(getattr(story, "period", "") or "UNE HISTOIRE EN IMAGES").upper()
    draw.text((width - margin - text_width(draw, period, load_font(14, bold=True)), 65), period, font=load_font(14, bold=True), fill=ACCENT)
    safe_rectangle(draw, (margin, 178, width - margin, 179), fill=MUTED)

    if not photos:
        draw.text((margin, 250), "AJOUTEZ DES PHOTOS POUR COMMENCER LA CHRONIQUE", font=load_font(14, bold=True), fill=MUTED)
        return

    hero_id = getattr(story, "hero_photo_id", "")
    hero = next((item for item in photos if item[0] == hero_id), photos[-1])
    archives = [item for item in photos if item[0] != hero[0]][:3]

    # The time line is a narrative spine; it remains useful even with two or three photos.
    line_y = 844
    line_left, line_right = margin, width - margin
    safe_rectangle(draw, (line_left, line_y, line_right, line_y + 1), fill=MUTED)
    points = [150, 350, 545, 860]
    for index, point_x in enumerate(points):
        safe_ellipse(draw, (point_x - 7, line_y - 7, point_x + 7, line_y + 7), fill=ACCENT if index < len(archives) + 1 else ACCENT_SOFT)

    archive_slots = [
        (70, 270, 166, 332, "01", "ORIGINES"),
        (290, 386, 206, 206, "02", "PASSAGE"),
        (518, 594, 188, 140, "03", "MÉMOIRE"),
    ]
    fallback_captions = ["ENFANCE", "JEUNE ADULTE", "SOUVENIR"]
    for index, item in enumerate(archives):
        _, image, caption = item
        x, y, photo_width, photo_height, number, fallback = archive_slots[index]
        framed_photo(canvas, image, x, y, photo_width, photo_height, border=6, archive=True)
        label(draw, number, caption or fallback_captions[index], x, y + photo_height + 20)
        draw.text((x, y + photo_height + 43), "CHAPITRE", font=load_font(9, bold=True), fill=MUTED)
        point_x = points[index]
        start_x = x + photo_width // 2
        start_y = min(line_y - 14, y + photo_height + 74)
        safe_polygon(
            draw,
            [(start_x - 1, start_y), (start_x + 1, start_y), (point_x + 1, line_y - 14), (point_x - 1, line_y - 14)],
            fill=ACCENT_SOFT,
        )

    hero_x, hero_y, hero_width, hero_height = 704, 270, 320, 475
    _, hero_image, hero_caption = hero
    framed_photo(canvas, hero_image, hero_x, hero_y, hero_width, hero_height, border=8, archive=False)
    label(draw, "04", hero_caption or "AUJOURD’HUI", hero_x, hero_y + hero_height + 23)
    place = str(getattr(story, "place", "") or "LE PRÉSENT").upper()
    draw.text((hero_x, hero_y + hero_height + 50), place, font=load_font(10, bold=True), fill=MUTED)
    draw.text((hero_x, hero_y + hero_height + 70), period, font=load_font(10), fill=MUTED)
    hero_start_x = hero_x + hero_width // 2
    hero_start_y = hero_y + hero_height + 98
    safe_polygon(
        draw,
        [(hero_start_x - 1, hero_start_y), (hero_start_x + 1, hero_start_y), (points[3] + 1, line_y - 14), (points[3] - 1, line_y - 14)],
        fill=ACCENT,
    )

    labels = ["01 / ORIGINES", "02 / PASSAGE", "03 / MÉMOIRE", "04 / PRÉSENT"]
    for point_x, item in zip(points, labels):
        used_font = load_font(10, bold=True)
        draw.text((point_x - text_width(draw, item, used_font) // 2, line_y + 21), item, font=used_font, fill=MUTED)

    safe_rectangle(draw, (margin, 963, width - margin, 964), fill=MUTED)
    footer = "UNE VIE RACONTÉE EN QUATRE CHAPITRES"
    draw.text((margin, 982), footer, font=load_font(10, bold=True), fill=MUTED)

