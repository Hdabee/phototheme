def _classic_cells(layout_id: str, size: int, gap: int):
    margin = gap
    half = (size - 3 * gap) // 2
    third = (size - 4 * gap) // 3

    if layout_id == "duo-split":
        return [(margin, margin, half, size - 2 * margin), (2 * margin + half, margin, half, size - 2 * margin)]
    if layout_id == "trio-story":
        height = (size - 4 * gap) // 3
        return [(margin, margin, size - 2 * margin, height), (margin, 2 * margin + height, size - 2 * margin, height), (margin, 3 * margin + 2 * height, size - 2 * margin, height)]
    if layout_id == "quad-classic":
        return [(margin, margin, half, half), (2 * margin + half, margin, half, half), (margin, 2 * margin + half, half, half), (2 * margin + half, 2 * margin + half, half, half)]
    if layout_id == "six-memory":
        return [(margin + (i % 3) * (third + gap), margin + (i // 3) * (third + gap), third, third) for i in range(6)]
    if layout_id == "nine-grid":
        return [(margin + (i % 3) * (third + gap), margin + (i // 3) * (third + gap), third, third) for i in range(9)]
    return None


def cells_for(layout_id: str, size: int, gap: int):
    classic = _classic_cells(layout_id, size, gap)
    if classic:
        return classic

    if layout_id == "timeline-three":
        width = (size - 4 * gap) // 3
        return [(gap + i * (width + gap), gap, width, size - 2 * gap) for i in range(3)]
    if layout_id == "timeline-four":
        width = (size - 5 * gap) // 4
        return [(gap + i * (width + gap), gap, width, size - 2 * gap) for i in range(4)]
    if layout_id == "gallery-three":
        hero_w = int(size * 0.60)
        side_w = size - hero_w - 3 * gap
        half_h = (size - 3 * gap) // 2
        return [(gap, gap, hero_w, size - 2 * gap), (2 * gap + hero_w, gap, side_w, half_h), (2 * gap + hero_w, 2 * gap + half_h, side_w, half_h)]
    if layout_id == "gallery-four":
        hero_w = int(size * 0.59)
        side_w = size - hero_w - 3 * gap
        third_h = (size - 4 * gap) // 3
        return [(gap, gap, hero_w, size - 2 * gap)] + [(2 * gap + hero_w, gap + i * (third_h + gap), side_w, third_h) for i in range(3)]
    if layout_id == "polaroid-three":
        return [(int(size * .08), int(size * .14), int(size * .54), int(size * .63)), (int(size * .39), int(size * .08), int(size * .52), int(size * .61)), (int(size * .24), int(size * .39), int(size * .55), int(size * .52))]
    if layout_id == "polaroid-four":
        return [(int(size * .07), int(size * .10), int(size * .43), int(size * .53)), (int(size * .50), int(size * .07), int(size * .42), int(size * .52)), (int(size * .12), int(size * .43), int(size * .43), int(size * .48)), (int(size * .50), int(size * .47), int(size * .41), int(size * .44))]
    if layout_id == "film-four":
        width = (size - 5 * gap) // 4
        height = int(size * .64)
        y = (size - height) // 2
        return [(gap + i * (width + gap), y, width, height) for i in range(4)]
    if layout_id == "film-six":
        width = (size - 4 * gap) // 3
        height = (size - 3 * gap) // 2
        return [(gap + (i % 3) * (width + gap), gap + (i // 3) * (height + gap), width, height) for i in range(6)]
    if layout_id == "story-three":
        return [(int(size * .08), int(size * .18), int(size * .38), int(size * .48)), (int(size * .45), int(size * .11), int(size * .43), int(size * .50)), (int(size * .28), int(size * .54), int(size * .46), int(size * .33))]
    if layout_id == "story-four":
        return [(int(size * .07), int(size * .25), int(size * .29), int(size * .36)), (int(size * .29), int(size * .12), int(size * .30), int(size * .39)), (int(size * .15), int(size * .61), int(size * .29), int(size * .25)), (int(size * .58), int(size * .18), int(size * .34), int(size * .59))]
    if layout_id == "atelier-three":
        return [(int(size * .08), int(size * .18), int(size * .38), int(size * .48)), (int(size * .45), int(size * .11), int(size * .43), int(size * .50)), (int(size * .28), int(size * .54), int(size * .46), int(size * .33))]
    if layout_id == "atelier-four":
        return [(int(size * .07), int(size * .25), int(size * .29), int(size * .36)), (int(size * .29), int(size * .12), int(size * .30), int(size * .39)), (int(size * .15), int(size * .61), int(size * .29), int(size * .25)), (int(size * .58), int(size * .18), int(size * .34), int(size * .59))]
    raise ValueError("Layout geometry inconnue.")


def rotations_for(layout_id: str, count: int):
    if layout_id == "polaroid-three":
        return [-3.0, 2.2, -1.4][:count]
    if layout_id == "polaroid-four":
        return [-2.5, 2.1, 1.7, -1.8][:count]
    if layout_id == "story-three":
        return [-4.0, 3.0, -2.0][:count]
    if layout_id == "story-four":
        return [-5.0, 2.0, -3.0, 1.0][:count]
    return [0.0] * count
