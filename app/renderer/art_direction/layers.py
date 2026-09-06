from PIL import Image, ImageDraw, ImageFilter, ImageFont

from app.renderer.art_direction.shapes import safe_polygon, safe_rectangle


def font(size, bold=False, serif=False):
    if serif:
        options = [
            "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
        ]
    elif bold:
        options = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/calibrib.ttf",
        ]
    else:
        options = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
        ]

    for path in options:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass

    return ImageFont.load_default()


def hex_rgba(value, alpha=255):
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4)) + (alpha,)


def paper(canvas, color, strength=12):
    draw = ImageDraw.Draw(canvas, "RGBA")

    for y in range(0, canvas.height, 6):
        draw.line(
            (0, y, canvas.width, y),
            fill=(80, 60, 35, strength if y % 12 else strength // 2),
        )

    for x in range(0, canvas.width, 35):
        draw.line(
            (x, 0, x, canvas.height),
            fill=(255, 255, 255, max(1, strength // 5)),
        )


def shadow_layer(width, height, opacity=55):
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")

    safe_rectangle(
        draw,
        (8, 10, width - 1, height - 1),
        fill=(28, 20, 12, opacity),
    )

    return layer.filter(ImageFilter.GaussianBlur(7))


def tape(canvas, x, y, width, angle=0):
    height = max(12, round(width * 0.33))
    strip = Image.new("RGBA", (width, height), (238, 211, 150, 165))
    strip = strip.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.alpha_composite(strip, (int(x - strip.width / 2), int(y - strip.height / 2)))


def torn_paper(width, height, color="#F8F1E3"):
    width = max(1, int(width))
    height = max(1, int(height))

    paper_image = Image.new("RGBA", (width, height), color)
    draw = ImageDraw.Draw(paper_image, "RGBA")

    points = [(0, 0), (width, 0)]

    for x in range(width, -1, -12):
        points.append((x, height - 5 - ((x * 17) % 11)))

    safe_polygon(draw, points, fill=color)

    return paper_image