from pathlib import Path
from app.editor.session_store import SessionStore

def test_split_three_vertical(tmp_path):
    source = tmp_path / "sheet.jpg"
    source.write_bytes(b"test")
    store = SessionStore()
    store.create("demo", [source])
    children = store.split_three_vertical("demo", "photo_0")
    assert len(children) == 3
    assert len(store.get("demo")) == 3
    assert children[0].crop_x == 0.0
    assert round(children[1].crop_x, 4) == round(1/3, 4)
    assert round(children[2].crop_x, 4) == round(2/3, 4)
