from app.renderer.art_direction.shapes import safe_rectangle
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from app.renderer.art_direction.shapes import rounded_mask, paste_masked
from app.renderer.image_ops import fit_cover

def load_font(size, bold=False, serif=False):
    candidates = []
    if serif:
        candidates += ["C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf"]
    else:
        candidates += ["C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()



from PIL import Image


def treatment(image, is_archive, dark=False):
    if is_archive:
        image = ImageEnhance.Color(image).enhance(0.72)
        image = ImageEnhance.Contrast(image).enhance(0.96)
        image = Image.blend(image, Image.new("RGB", image.size, "#D7C2A0"), 0.07)
    else:
        image = ImageEnhance.Contrast(image).enhance(1.04)
        image = ImageEnhance.Color(image).enhance(0.97)
    if dark:
        image = ImageEnhance.Brightness(image).enhance(0.93)
    return image


def text_center(draw, text, x, y, width, font, fill):
    bounds = draw.textbbox((0, 0), text, font=font)
    draw.text((x + (width - (bounds[2] - bounds[0])) // 2, y), text, font=font, fill=fill)


def draw_photo(canvas, photo, x, y, width, height, border_color, border_width=7):
    photo = fit_cover(photo, width, height)
    frame = Image.new("RGBA", (width + 2 * border_width, height + 2 * border_width), border_color)
    frame.paste(photo.convert("RGBA"), (border_width, border_width))
    canvas.alpha_composite(frame, (x - border_width, y - border_width))


def render_editorial_timeline(canvas, photos, story, dark=False):
    width, height = canvas.size
    draw = ImageDraw.Draw(canvas, "RGBA")
    background = "#20201E" if dark else "#F2EFE8"
    ink = (239, 234, 223, 255) if dark else (42, 39, 34, 255)
    muted = (191, 181, 164, 255) if dark else (106, 96, 82, 255)
    accent = (196, 94, 61, 255)
    frame = "#34332F" if dark else "#FFFCF5"

    safe_rectangle(draw, (0, 0, width, height), fill=background)

    safe = 56
    header_bottom = 190
    footer_top = 945
    divider_x = 635

    draw.text((safe, 58), str(story.title).upper(), font=load_font(43, bold=True, serif=True), fill=ink)
    draw.text((safe, 116), str(story.subtitle), font=load_font(18), fill=muted)
    draw.text((width - 215, 64), str(story.period).upper(), font=load_font(15, bold=True), fill=accent)
    draw.line((safe, header_bottom, width - safe, header_bottom), fill=muted, width=2)

    draw.text((safe, 215), "ARCHIVES", font=load_font(13, bold=True), fill=accent)
    draw.text((divider_x + 25, 215), "AUJOURD'HUI", font=load_font(13, bold=True), fill=accent)
    draw.line((divider_x, 240, divider_x, footer_top - 42), fill=muted, width=2)

    if not photos:
        return

    hero = next((item for item in photos if item[0] == story.hero_photo_id), photos[-1])
    archives = [item for item in photos if item[0] != hero[0]][:3]
    archive_positions = [(safe, 286), (242, 286), (428, 286)]
    archive_width, archive_height = 150, 455

    labels = ["ENFANCE", "JEUNE ADULTE", "PORTRAIT"]
    for index, item in enumerate(archives):
        _, image, caption = item
        x, y = archive_positions[index]
        image = treatment(image, is_archive=True, dark=dark)
        draw_photo(canvas, image, x, y, archive_width, archive_height, frame, border_width=6)
        draw.text((x, 767), f"{index + 1:02d}", font=load_font(15, bold=True), fill=accent)
        draw.text((x + 30, 768), (caption or labels[index]).upper(), font=load_font(12, bold=True), fill=ink)
        draw.text((x, 796), "CHAPITRE", font=load_font(10), fill=muted)

    _, hero_image, hero_caption = hero
    hero_x, hero_y, hero_width, hero_height = 690, 286, 332, 530
    hero_image = treatment(hero_image, is_archive=False, dark=dark)
    draw_photo(canvas, hero_image, hero_x, hero_y, hero_width, hero_height, frame, border_width=8)
    draw.text((hero_x, 846), "04", font=load_font(15, bold=True), fill=accent)
    draw.text((hero_x + 32, 847), (hero_caption or "AUJOURD'HUI").upper(), font=load_font(13, bold=True), fill=ink)
    draw.text((hero_x, 876), str(story.place).upper(), font=load_font(10), fill=muted)

    draw.line((safe, footer_top, width - safe, footer_top), fill=muted, width=2)
    draw.text((safe, footer_top + 18), "01 / ORIGINES", font=load_font(11, bold=True), fill=muted)
    draw.text((328, footer_top + 18), "02 / PASSAGE", font=load_font(11, bold=True), fill=muted)
    draw.text((548, footer_top + 18), "03 / MÉMOIRE", font=load_font(11, bold=True), fill=muted)
    draw.text((770, footer_top + 18), "04 / PRÉSENT", font=load_font(11, bold=True), fill=muted)


def render_portrait_timeline_editorial(canvas, photos, story):
    render_editorial_timeline(canvas, photos, story, dark=False)


def render_editorial_night(canvas, photos, story):
    render_editorial_timeline(canvas, photos, story, dark=True)
