from app.renderer.art_direction.shapes import safe_ellipse, safe_rectangle
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
from app.renderer.art_direction.layers import font, paper, tape, torn_paper


def stylize(photo, theme_id):
    if theme_id == "archive-vivante":
        photo = ImageEnhance.Color(photo).enhance(0.68)
        photo = ImageEnhance.Contrast(photo).enhance(0.94)
        return Image.blend(photo, Image.new("RGB", photo.size, "#D9BA89"), 0.10)
    if theme_id == "editorial-magazine":
        photo = ImageEnhance.Color(photo).enhance(0.82)
        return ImageEnhance.Contrast(photo).enhance(1.13)
    if theme_id == "scrapbook-authentique":
        photo = ImageEnhance.Brightness(photo).enhance(1.06)
        return Image.blend(photo, Image.new("RGB", photo.size, "#EFCB90"), 0.08)
    if theme_id == "contact-sheet-archive":
        photo = ImageOps.grayscale(photo).convert("RGB")
        return ImageEnhance.Contrast(photo).enhance(1.35)
    if theme_id == "retro-sunshine":
        photo = ImageEnhance.Color(photo).enhance(1.22)
        photo = ImageEnhance.Contrast(photo).enhance(1.12)
        return Image.blend(photo, Image.new("RGB", photo.size, "#E56733"), 0.08)
    return photo


def background(canvas, theme_id):
    draw = ImageDraw.Draw(canvas, "RGBA")
    width, height = canvas.size

    if theme_id == "archive-vivante":
        paper(canvas, "#EDE4D4", 14)
        safe_rectangle(draw, (28, 28, width - 29, height - 29), outline=(104, 76, 48, 90), width=2)
        draw.text((54, 48), "UNE VIE EN IMAGES", font=font(25, serif=True), fill=(66, 50, 35, 255))
        draw.text(
            (56, 80),
            "FRAGMENTS / SOUVENIRS / AUJOURD'HUI",
            font=font(12, bold=True),
            fill=(90, 70, 49, 190),
        )
        draw.line((width * 0.52, 150, width * 0.52, height - 110), fill=(103, 75, 46, 145), width=3)
        draw.text((width * 0.52 + 13, height * 0.47), "THEN -> NOW", font=font(14, bold=True), fill=(93, 66, 41, 220))

    elif theme_id == "editorial-magazine":
        safe_rectangle(draw, (25, 25, width - 26, height - 26), outline=(35, 35, 31, 255), width=3)
        draw.text((55, 48), "PORTRAIT", font=font(78, bold=True), fill=(27, 27, 24, 255))
        draw.text((58, 132), "VOL. 01 - UNE VIE EN QUATRE REGARDS", font=font(16, bold=True), fill=(27, 27, 24, 210))
        draw.multiline_text(
            (width - 170, 55),
            "2026\nPHOTO\nESSAY",
            font=font(14, bold=True),
            fill=(27, 27, 24, 220),
            spacing=4,
        )
        draw.line((55, 168, width - 55, 168), fill=(27, 27, 24, 130), width=2)

    elif theme_id == "scrapbook-authentique":
        paper(canvas, "#D7C4A7", 18)
        torn_paper(canvas, 50, 70, 300, 170, (247, 236, 209, 255))
        torn_paper(canvas, width - 290, height - 240, 240, 155, (235, 215, 176, 255))
        draw.text((65, 80), "little things", font=font(30, serif=True), fill=(83, 60, 42, 255))
        draw.text((68, 117), "A COLLECTION OF MOMENTS", font=font(12, bold=True), fill=(97, 70, 45, 200))

    elif theme_id == "contact-sheet-archive":
        safe_rectangle(draw, (18, 18, width - 19, height - 19), outline=(235, 221, 185, 180), width=2)
        for y in (10, height - 19):
            for x in range(25, width - 25, 28):
                safe_rectangle(draw, (x, y, x + 14, y + 7), fill=(237, 220, 178, 230))
        draw.text((42, 38), "PHOTOTHEME ARCHIVE / ROLL 04", font=font(18, bold=True), fill=(238, 225, 195, 255))
        draw.text((width - 190, 40), "CONTACT SHEET", font=font(13, bold=True), fill=(238, 225, 195, 180))

    elif theme_id == "retro-sunshine":
        for radius, color in [(520, (244, 201, 82, 255)), (390, (232, 126, 49, 255)), (260, (172, 66, 42, 255))]:
            safe_ellipse(draw, (width - radius // 2, -radius // 2, width + radius // 2, radius // 2), fill=color)
        safe_rectangle(draw, (32, 32, width - 33, height - 33), outline=(86, 55, 37, 180), width=3)
        draw.text((55, height - 132), "GOOD TIMES", font=font(62, bold=True), fill=(83, 51, 33, 255))
        draw.text((60, height - 75), "POSTCARD FROM THE PAST", font=font(15, bold=True), fill=(83, 51, 33, 220))


def overlays(canvas, theme_id, states, cells):
    draw = ImageDraw.Draw(canvas, "RGBA")
    width, height = canvas.size

    if theme_id == "archive-vivante":
        labels = ["ENFANCE", "JEUNE ADULTE", "PORTRAIT", "AUJOURD'HUI"]
        for index, (x, y, cell_w, cell_h) in enumerate(cells):
            label = states[index].caption or labels[min(index, 3)]
            draw.text((x, y + cell_h + 24), label, font=font(15, serif=True), fill=(65, 48, 34, 255))
            draw.text((x, y + cell_h + 44), f"0{index + 1} / CHAPITRE", font=font(10, bold=True), fill=(95, 74, 52, 190))

    elif theme_id == "editorial-magazine":
        for index, (x, y, cell_w, cell_h) in enumerate(cells):
            draw.text((x, y + cell_h + 12), f"{index + 1:02d}", font=font(18, bold=True), fill=(25, 25, 23, 255))
            if states[index].caption:
                draw.text((x + 30, y + cell_h + 15), states[index].caption.upper(), font=font(11, bold=True), fill=(25, 25, 23, 215))

    elif theme_id == "scrapbook-authentique":
        for index, (x, y, cell_w, cell_h) in enumerate(cells):
            tape(canvas, x + cell_w // 3, y - 12, max(70, cell_w // 2), -6 if index % 2 == 0 else 5)
            if states[index].caption:
                draw.text((x + 10, y + cell_h + 18), states[index].caption, font=font(16, serif=True), fill=(79, 56, 36, 255))
        draw.text((width - 230, height - 70), "KEEP THIS CLOSE", font=font(14, bold=True), fill=(91, 64, 38, 210))

    elif theme_id == "contact-sheet-archive":
        for index, (x, y, cell_w, cell_h) in enumerate(cells):
            label = states[index].caption or "FRAME"
            draw.text((x + 2, y + cell_h + 20), f"N {index + 1:02d}  {label}", font=font(12, bold=True), fill=(238, 225, 195, 230))
        if cells:
            x, y, cell_w, cell_h = cells[-1]
            safe_rectangle(draw, (x - 5, y - 5, x + cell_w + 5, y + cell_h + 5), outline=(204, 73, 54, 255), width=3)

    elif theme_id == "retro-sunshine":
        for index, (x, y, cell_w, cell_h) in enumerate(cells):
            label = states[index].caption or f"MEMORY {index + 1}"
            draw.text((x + 8, y + cell_h + 18), label, font=font(14, bold=True), fill=(82, 50, 33, 255))
        draw.multiline_text(
            (width - 180, 105),
            "1970\nSUMMER\nEDITION",
            font=font(15, bold=True),
            fill=(83, 51, 33, 230),
            spacing=5,
        )
