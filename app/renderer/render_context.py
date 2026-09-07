from dataclasses import dataclass
from typing import Any

from PIL import Image

from app.editor.photo_state import PhotoEditState
from app.editor.project_story import ProjectStoryState


@dataclass
class RenderContext:
    """Immutable-by-convention input passed to every theme renderer."""

    canvas: Image.Image
    states: list[PhotoEditState]
    rendered: list[tuple[str, Image.Image, str]]
    layout: dict[str, Any]
    theme: dict[str, Any]
    story: ProjectStoryState
    size: int
