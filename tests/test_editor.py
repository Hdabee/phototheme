from PIL import Image
from app.editor.photo_state import PhotoEditState
from app.editor.photo_transformer import transform_photo

def test_transform_photo_rotation_and_enhancement():
    image = Image.new("RGB", (80, 40), "red")
    state = PhotoEditState(photo_id="one", source_path="unused", rotation=90, brightness=1.1, contrast=1.1)
    result = transform_photo(image, state)
    assert result.size == (40, 80)

def test_photo_state_defaults():
    state = PhotoEditState(photo_id="one", source_path="source.png")
    assert state.fit_mode == "contain"
    assert state.brightness == 1.0
