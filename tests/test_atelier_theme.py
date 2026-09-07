from app.renderer.art_direction import atelier
from app.renderer.image_ops import fit_cover


def test_atelier_uses_shared_fit_cover():
    assert atelier.fit_cover is fit_cover
