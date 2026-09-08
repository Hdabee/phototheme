from PIL import Image, ImageDraw, ImageEnhance

from app.renderer.art_direction.layers import font, shadow_layer
from app.renderer.art_direction.shapes import (
    draw_leaf,
    paste_masked,
    rounded_mask,
    safe_ellipse,
    safe_rectangle,
    safe_rounded_rectangle,
    ticket_mask,
)

from app.renderer.image_ops import fit_cover


BACKGROUND = (76, 106, 88, 255)
CREAM = (245, 232, 201, 255)
CREAM_SOFT = (245, 232, 201, 225)
PINK = (201, 104, 108, 255)
TERRACOTTA = (184, 86, 62, 255)
FOREST = (37, 68, 52, 220)
SHADOW = (39, 53, 44, 255)



def prepared(image):
    image = ImageEnhance.Color(image).enhance(1.06)
    image = ImageEnhance.Contrast(image).enhance(1.04)
    return Image.blend(image, Image.new("RGB", image.size, "#F0C58F"), 0.045)


def label(draw, text, x, y, size=12, fill=CREAM_SOFT):
    draw.text((x, y), str(text).upper(), font=font(size, bold=True), fill=fill)


def render_garden(canvas, photos, story):
    width, height = canvas.size
    draw = ImageDraw.Draw(canvas, "RGBA")

    safe_rectangle(draw, (0, 0, width, height), fill=BACKGROUND)
    safe_rectangle(draw, (34, 34, width - 35, height - 35), outline=CREAM_SOFT, width=4)

    # Decorative botanical forms, deliberately outside the main image/text zones.
    safe_ellipse(draw, (width - 260, -100, width + 96, 250), fill=(201, 104, 108, 120))
    safe_ellipse(draw, (width - 190, -44, width + 44, 188), fill=(184, 86, 62, 150))
    safe_ellipse(draw, (70, 182, 148, 244), fill=(37, 68, 52, 225))
    draw_leaf(canvas, width - 120, 245, 132, FOREST, sign=-1)
    draw_leaf(canvas, 68, 800, 150, FOREST)
    draw_leaf(canvas, width - 62, 870, 118, (201, 104, 108, 190), sign=-1)

    title = str(getattr(story, "title", "") or "JARDIN D'ÉTÉ").upper()
    subtitle = str(getattr(story, "subtitle", "") or "LUMIÈRE, FEUILLAGE ET SOUVENIRS").upper()
    period = str(getattr(story, "period", "") or "ÉTÉ 2026").upper()
    place = str(getattr(story, "place", "") or "UN LIEU · QUATRE REGARDS").upper()

    draw.text((58, 54), title, font=font(51, bold=True), fill=CREAM)
    draw.text((61, 119), subtitle, font=font(15, bold=True), fill=CREAM_SOFT)
    draw.text((width - 202, 61), period, font=font(14, bold=True), fill=CREAM_SOFT)

    if not photos:
        label(draw, place, 55, height - 69, 14)
        return

    hero_id = getattr(story, "hero_photo_id", "")
    hero = next((photo for photo in photos if photo[0] == hero_id), photos[-1])
    others = [photo for photo in photos if photo[0] != hero[0]][:3]

    _, hero_image, hero_caption = hero
    hero_width, hero_height = 590, 405
    hero_x, hero_y = 245, 248
    hero_image = prepared(fit_cover(hero_image, hero_width, hero_height))

    canvas.alpha_composite(shadow_layer(hero_width, hero_height, 76), (hero_x + 10, hero_y + 12))
    paste_masked(canvas, hero_image, hero_x, hero_y, rounded_mask(hero_width, hero_height, 34))
    safe_rounded_rectangle(
        draw,
        (hero_x - 7, hero_y - 7, hero_x + hero_width + 7, hero_y + hero_height + 7),
        radius=40,
        outline=CREAM,
        width=7,
    )
    label(draw, hero_caption or "LA MAISON EN FLEURS", hero_x, hero_y + hero_height + 25, 18, CREAM)
    label(draw, "JARDIN D'ÉTÉ", hero_x, hero_y + hero_height + 51, 11, CREAM_SOFT)

    positions = [
        (76, 716, 242, 150, -4),
        (419, 770, 242, 150, 0),
        (763, 716, 242, 150, 4),
    ]
    fallback_labels = ["FAÇADE", "JARDIN", "FLORAISON"]

    for index, item in enumerate(others):
        _, image, caption = item
        x, y, cell_width, cell_height, rotation = positions[index]
        photo = prepared(fit_cover(image, cell_width, cell_height))
        mask = ticket_mask(cell_width, cell_height, cut=16)
        layer = Image.new("RGBA", (cell_width, cell_height), (0, 0, 0, 0))
        layer.paste(photo.convert("RGBA"), (0, 0), mask)
        if rotation:
            layer = layer.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
        canvas.alpha_composite(shadow_layer(layer.width, layer.height, 52), (x, y + 7))
        canvas.alpha_composite(layer, (x, y))
        label(draw, caption or fallback_labels[index], x + 10, y + cell_height + 13, 12, CREAM)

    # When the 3-photo layout is selected, retain intentional balance in the third memory zone.
    if len(others) == 2:
        safe_ellipse(draw, (846, 757, 920, 831), outline=PINK, width=4)
        safe_ellipse(draw, (867, 778, 899, 810), fill=PINK)
        label(draw, "ÉTÉ", 842, 880, 11, CREAM_SOFT)

    safe_rectangle(draw, (55, height - 86, width - 55, height - 85), fill=CREAM_SOFT)
    label(draw, place, 55, height - 67, 14, CREAM)
    label(draw, period, width - 174, height - 67, 13, CREAM_SOFT)
