from pathlib import Path

FORBIDDEN = (".ellipse(", ".rectangle(", ".rounded_rectangle(", ".polygon(")
ROOT = Path(__file__).resolve().parents[1]
ART_DIRECTION = ROOT / "app" / "renderer" / "art_direction"


def test_only_shapes_module_calls_pillow_shape_primitives_directly():
    violations = []
    for path in ART_DIRECTION.glob("*.py"):
        if path.name == "shapes.py":
            continue
        source = path.read_text(encoding="utf-8")
        for primitive in FORBIDDEN:
            if primitive in source:
                violations.append(f"{path.name}: {primitive}")
    assert not violations, "Primitives Pillow non securisees : " + ", ".join(violations)
