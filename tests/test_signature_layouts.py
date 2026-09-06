from app.renderer.layout_geometry import cells_for, rotations_for


def test_gallery_four_has_one_tall_hero_and_three_side_cells():
    cells = cells_for("gallery-four", 1000, 10)
    assert len(cells) == 4
    assert cells[0][2] > cells[1][2]
    assert cells[0][3] > cells[1][3]


def test_polaroid_has_rotation_variation():
    rotations = rotations_for("polaroid-four", 4)
    assert len(rotations) == 4
    assert any(value != 0 for value in rotations)


def test_timeline_four_has_four_cells():
    assert len(cells_for("timeline-four", 1000, 10)) == 4
