from app.renderer.art_direction.shapes import safe_ellipse, safe_rectangle, safe_rounded_rectangle
from PIL import Image, ImageDraw, ImageEnhance
from app.renderer.art_direction.layers import font, paper, shadow_layer
from app.renderer.art_direction.shapes import draw_leaf, draw_sun, ellipse_mask, paste_masked, rounded_mask, ticket_mask


def fit_cover(image, width, height):
    ratio = image.width / image.height
    target = width / height
    new_width, new_height = (round(height * ratio), height) if ratio > target else (width, round(width / ratio))
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left, top = (new_width - width) // 2, (new_height - height) // 2
    return image.crop((left, top, left + width, top + height))


def prepared(image, theme_id):
    if theme_id == "reconstructed-portrait":
        return ImageEnhance.Contrast(ImageEnhance.Color(image).enhance(0.76)).enhance(1.12)
    image = ImageEnhance.Color(image).enhance(1.16)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    return Image.blend(image, Image.new("RGB", image.size, "#EF9C55"), 0.07)


def card(canvas, image, x, y, width, height, rotation=0, border="#FFF8E8", shadow=True, mask=None):
    photo = fit_cover(image, width, height)

    if mask is not None:
        photo_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        photo_layer.paste(photo.convert("RGBA"), (0, 0), mask)
        if shadow:
            canvas.alpha_composite(shadow_layer(width, height, 70), (x + 7, y + 8))
        canvas.alpha_composite(photo_layer, (x, y))
        return

    frame = 14
    panel = Image.new("RGBA", (width + frame * 2, height + frame * 2 + 18), border)
    panel.paste(photo.convert("RGBA"), (frame, frame))
    if rotation:
        panel = panel.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
    if shadow:
        canvas.alpha_composite(
            shadow_layer(panel.width, panel.height, 65),
            (x - frame - (panel.width - (width + frame * 2)) // 2 + 6, y - frame - (panel.height - (height + frame * 2 + 18)) // 2 + 8),
        )
    canvas.alpha_composite(
        panel,
        (x - frame - (panel.width - (width + frame * 2)) // 2, y - frame - (panel.height - (height + frame * 2 + 18)) // 2),
    )


def render_reconstructed(canvas, photos, story):
    width, height = canvas.size
    draw = ImageDraw.Draw(canvas, "RGBA")
    paper(canvas, "#E7D9C6", 10)
    safe_rectangle(draw, (28, 28, width - 29, height - 29), outline=(40, 36, 32, 150), width=2)
    draw.text((52, 48), str(story.title).upper(), font=font(48, bold=True), fill=(33, 31, 29, 255))
    draw.text((56, 107), str(story.subtitle).upper(), font=font(14, bold=True), fill=(86, 65, 50, 220))
    draw.text((58, 137), str(story.period), font=font(18, serif=True), fill=(140, 69, 46, 255))
    safe_rectangle(draw, (52, 180, 390, 218), fill=(180, 75, 51, 235))
    draw.text((63, 190), str(story.place).upper(), font=font(14, bold=True), fill=(255, 247, 232, 255))

    if not photos:
        return

    hero = next((photo for photo in photos if photo[0] == story.hero_photo_id), photos[-1])
    archives = [photo for photo in photos if photo[0] != hero[0]][:3]
    positions = [(72, 285, 250, 305, -7), (268, 360, 225, 275, 5), (110, 650, 235, 245, -3)]

    for index, item in enumerate(archives):
        _, image, caption = item
        x, y, cell_width, cell_height, rotation = positions[index]
        card(canvas, prepared(image, "reconstructed-portrait"), x, y, cell_width, cell_height, rotation, border="#FFF8EE")
        draw.text((x, y + cell_height + 38), caption or f"ARCHIVE {index + 1:02d}", font=font(14, serif=True), fill=(48, 41, 35, 255))

    _, hero_image, hero_caption = hero
    hero_width, hero_height = 420, 520
    hero_x, hero_y = 610, 255
    hero_image = prepared(fit_cover(hero_image, hero_width, hero_height), "reconstructed-portrait")
    canvas.alpha_composite(shadow_layer(hero_width, hero_height, 90), (hero_x + 10, hero_y + 12))
    paste_masked(canvas, hero_image, hero_x, hero_y, ellipse_mask(hero_width, hero_height))
    safe_ellipse(draw, (hero_x - 8, hero_y - 8, hero_x + hero_width + 8, hero_y + hero_height + 8), outline=(180, 75, 51, 255), width=7)
    draw.text((hero_x, hero_y + hero_height + 25), hero_caption or "AUJOURD'HUI", font=font(22, bold=True), fill=(40, 35, 30, 255))
    draw.text((hero_x, hero_y + hero_height + 55), "THE PORTRAIT THAT HOLDS THE STORY", font=font(11, bold=True), fill=(105, 76, 56, 220))
    draw.text((525, 780), "THEN", font=font(21, bold=True), fill=(180, 75, 51, 255))
    draw.line((525, 813, 665, 813), fill=(180, 75, 51, 255), width=4)
    draw.text((675, 800), "NOW", font=font(21, bold=True), fill=(180, 75, 51, 255))


def render_island(canvas, photos, story):
    width, height = canvas.size
    draw = ImageDraw.Draw(canvas, "RGBA")
    safe_rectangle(draw, (0, 0, width, height), fill=(23, 123, 141, 255))
    draw_sun(canvas, width - 130, 115, [260, 196, 134], [(245, 185, 66, 255), (225, 103, 50, 255), (180, 66, 43, 255)])
    draw_leaf(canvas, 100, 250, 210, (34, 95, 71, 210))
    draw_leaf(canvas, width - 85, 310, 170, (34, 95, 71, 210), True)
    safe_rectangle(draw, (34, 34, width - 35, height - 35), outline=(247, 225, 184, 220), width=4)
    draw.text((58, 54), str(story.title).upper() or "ISLAND DAYS", font=font(55, bold=True), fill=(255, 240, 202, 255))
    draw.text((61, 119), str(story.subtitle).upper(), font=font(15, bold=True), fill=(255, 240, 202, 230))

    if not photos:
        return

    hero = next((photo for photo in photos if photo[0] == story.hero_photo_id), photos[-1])
    others = [photo for photo in photos if photo[0] != hero[0]][:3]
    _, hero_image, hero_caption = hero
    hero_width, hero_height = 590, 420
    hero_x, hero_y = 245, 245
    hero_image = prepared(fit_cover(hero_image, hero_width, hero_height), "island-poster")
    canvas.alpha_composite(shadow_layer(hero_width, hero_height, 75), (hero_x + 9, hero_y + 11))
    paste_masked(canvas, hero_image, hero_x, hero_y, rounded_mask(hero_width, hero_height, 32))
    safe_rounded_rectangle(draw, (hero_x - 7, hero_y - 7, hero_x + hero_width + 7, hero_y + hero_height + 7), radius=38, outline=(255, 239, 200, 255), width=7)
    draw.text((hero_x, hero_y + hero_height + 25), hero_caption or "THE MAIN MEMORY", font=font(18, bold=True), fill=(255, 242, 211, 255))

    ticket_positions = [(75, 700, 250, 165, -5), (755, 700, 250, 165, 5), (405, 775, 250, 165, -2)]
    for index, item in enumerate(others):
        _, image, caption = item
        x, y, cell_width, cell_height, rotation = ticket_positions[index]
        ticket = prepared(fit_cover(image, cell_width, cell_height), "island-poster")
        layer = Image.new("RGBA", (cell_width, cell_height), (0, 0, 0, 0))
        layer.paste(ticket.convert("RGBA"), (0, 0), ticket_mask(cell_width, cell_height))
        if rotation:
            layer = layer.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
        canvas.alpha_composite(shadow_layer(layer.width, layer.height, 55), (x, y + 7))
        canvas.alpha_composite(layer, (x, y))
        draw.text((x + 12, y + cell_height + 13), caption or f"MEMORY {index + 1}", font=font(12, bold=True), fill=(255, 239, 200, 255))

    draw.text((55, height - 72), str(story.place).upper(), font=font(15, bold=True), fill=(255, 239, 200, 255))
    draw.text((55, height - 43), str(story.period).upper(), font=font(13, bold=True), fill=(255, 239, 200, 215))


def render_atelier(canvas, theme_id, photos, story):
    if theme_id == "reconstructed-portrait":
        render_reconstructed(canvas, photos, story)
    elif theme_id == "island-poster":
        render_island(canvas, photos, story)
