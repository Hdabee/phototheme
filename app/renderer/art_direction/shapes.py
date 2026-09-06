from PIL import Image, ImageDraw


def safe_box(x0, y0, x1, y1):
    """Return an integer Pillow box with non-inverted coordinates."""
    left, right = sorted((int(round(x0)), int(round(x1))))
    top, bottom = sorted((int(round(y0)), int(round(y1))))
    return left, top, right, bottom


def safe_ellipse(draw, xy, **kwargs):
    return draw.ellipse(safe_box(*xy), **kwargs)


def safe_rectangle(draw, xy, **kwargs):
    return draw.rectangle(safe_box(*xy), **kwargs)


def safe_rounded_rectangle(draw, xy, radius=0, **kwargs):
    left, top, right, bottom = safe_box(*xy)
    maximum_radius = max(0, min((right - left) // 2, (bottom - top) // 2))
    radius = max(0, min(int(round(radius)), maximum_radius))
    return draw.rounded_rectangle(
        (left, top, right, bottom),
        radius=radius,
        **kwargs,
    )


def safe_polygon(draw, points, **kwargs):
    normalized = [(int(round(x)), int(round(y))) for x, y in points]
    return draw.polygon(normalized, **kwargs)


def rounded_mask(width, height, radius):
    width = max(1, int(width))
    height = max(1, int(height))
    radius = max(0, min(int(round(radius)), width // 2, height // 2))
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, width - 1, height - 1),
        radius=radius,
        fill=255,
    )
    return mask


def ellipse_mask(width, height):
    """Compatibility helper used by Atelier and its tests."""
    width = max(1, int(width))
    height = max(1, int(height))
    mask = Image.new("L", (width, height), 0)
    safe_ellipse(
        ImageDraw.Draw(mask),
        (0, 0, width - 1, height - 1),
        fill=255,
    )
    return mask


def ticket_mask(width, height, cut=18):
    """Ticket-shaped mask with safe semicircular side notches."""
    width = max(1, int(width))
    height = max(1, int(height))
    cut = max(0, int(round(cut)))
    mask = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(mask)

    if cut > 0:
        middle = height // 2
        safe_ellipse(draw, (-cut, middle - cut, cut, middle + cut), fill=0)
        safe_ellipse(draw, (width - cut, middle - cut, width + cut, middle + cut), fill=0)

    return mask


def paste_masked(canvas, image, x, y, mask_or_width, height=None, radius=0):
    """Paste an image using either an existing mask or width/height arguments.

    Supported signatures:
    - paste_masked(canvas, image, x, y, mask)
    - paste_masked(canvas, image, x, y, width, height, radius=0)
    """

    x = int(round(x))
    y = int(round(y))

    # Historical Atelier signature: a ready-to-use PIL mask.
    if isinstance(mask_or_width, Image.Image):
        mask = mask_or_width.convert("L")
        width, height = mask.size

        fitted = image.resize(
            (max(1, width), max(1, height)),
            Image.Resampling.LANCZOS,
        ).convert("RGBA")

        canvas.paste(fitted, (x, y), mask)
        return None

    # Modern signature: width, height, optional corner radius.
    width = max(1, int(mask_or_width))
    height = max(1, int(height))

    fitted = image.resize(
        (width, height),
        Image.Resampling.LANCZOS,
    ).convert("RGBA")

    mask = rounded_mask(width, height, radius)
    canvas.paste(fitted, (x, y), mask)

    return None

def circle(draw, cx, cy, radius, **kwargs):
    radius = abs(float(radius))
    return safe_ellipse(
        draw,
        (cx - radius, cy - radius, cx + radius, cy + radius),
        **kwargs,
    )


def pill(draw, x0, y0, x1, y1, radius=0, **kwargs):
    return safe_rounded_rectangle(draw, (x0, y0, x1, y1), radius=radius, **kwargs)


def draw_sun(draw_or_canvas, cx, cy, radius_or_rings, color_or_palette, rays=0, ray_length=None, ray_width=3):
    """Draw a safe sun and preserve the historical Island Poster API.

    Supported signatures:
    - draw_sun(draw, cx, cy, radius, color, rays=0, ...)
    - draw_sun(canvas, cx, cy, [outer, middle, inner], [outer_color, middle_color, inner_color])
    """
    draw = (
        draw_or_canvas
        if hasattr(draw_or_canvas, "ellipse")
        else ImageDraw.Draw(draw_or_canvas, "RGBA")
    )

    if isinstance(radius_or_rings, (list, tuple)):
        radii = [
            abs(float(value))
            for value in radius_or_rings
            if isinstance(value, (int, float))
        ]
        palette = (
            list(color_or_palette)
            if isinstance(color_or_palette, (list, tuple))
            else [color_or_palette]
        )

        if not radii or not palette:
            return None

        for index, radius in enumerate(radii):
            color = palette[index] if index < len(palette) else palette[-1]

            safe_ellipse(
                draw,
                (cx - radius, cy - radius, cx + radius, cy + radius),
                fill=color,
            )

        return None

    radius = abs(float(radius_or_rings))

    safe_ellipse(
        draw,
        (cx - radius, cy - radius, cx + radius, cy + radius),
        fill=color_or_palette,
    )

    if rays:
        import math

        length = (
            radius * 0.55
            if ray_length is None
            else max(0, float(ray_length))
        )
        ray_count = max(1, int(rays))
        thickness = max(1, int(ray_width))

        for index in range(ray_count):
            angle = (2 * math.pi * index) / ray_count
            start_distance = radius + max(2, thickness)
            end_distance = start_distance + length

            x0 = int(round(cx + math.cos(angle) * start_distance))
            y0 = int(round(cy + math.sin(angle) * start_distance))
            x1 = int(round(cx + math.cos(angle) * end_distance))
            y1 = int(round(cy + math.sin(angle) * end_distance))

            draw.line(
                (x0, y0, x1, y1),
                fill=color_or_palette,
                width=thickness,
            )

    return None

def draw_leaf(draw_or_canvas, points_or_x, y=None, scale=None, color=None, sign=1):
    """Draw a safe leaf; accepts either ImageDraw or PIL Image canvas.

    Supported signatures:
    - draw_leaf(draw, x, y, scale, color, sign=1)
    - draw_leaf(canvas, x, y, scale, color, sign=1)
    - draw_leaf(draw_or_canvas, [(x1, y1), ...], color)
    """

    draw = (
        draw_or_canvas
        if hasattr(draw_or_canvas, "ellipse")
        else ImageDraw.Draw(draw_or_canvas, "RGBA")
    )

    # Historical polygon form: draw_leaf(canvas_or_draw, points, color)
    if isinstance(points_or_x, (list, tuple)) and points_or_x:
        points = points_or_x

        if color is None and y is not None:
            color = y

        normalized = [
            (int(round(point[0])), int(round(point[1])))
            for point in points
            if isinstance(point, (list, tuple)) and len(point) >= 2
        ]

        if len(normalized) >= 3:
            return safe_polygon(
                draw,
                normalized,
                fill=color or (58, 112, 70, 255),
            )

        return None

    # Numeric form used by Island Poster.
    x = float(points_or_x)
    y = float(y)
    scale = abs(float(scale))
    sign = -1 if sign < 0 else 1

    return safe_ellipse(
        draw,
        (
            x,
            y - scale * 0.18,
            x + sign * scale * 0.36,
            y + scale * 0.04,
        ),
        fill=color or (58, 112, 70, 255),
    )
