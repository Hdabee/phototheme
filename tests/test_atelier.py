from app.editor.project_story import ProjectStoryState
from app.renderer.art_direction.shapes import ellipse_mask, ticket_mask

def test_story_default_has_title():
    assert ProjectStoryState().title

def test_ellipse_mask_has_expected_size():
    assert ellipse_mask(120, 80).size == (120, 80)

def test_ticket_mask_has_expected_size():
    assert ticket_mask(120, 80).size == (120, 80)
