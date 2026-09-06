from dataclasses import asdict, dataclass

@dataclass
class PhotoEditState:
    photo_id: str
    source_path: str
    crop_x: float = 0.0
    crop_y: float = 0.0
    crop_width: float = 1.0
    crop_height: float = 1.0
    fit_mode: str = "contain"
    rotation: int = 0
    flip_horizontal: bool = False
    brightness: float = 1.0
    contrast: float = 1.0
    saturation: float = 1.0
    sharpness: float = 1.0
    caption: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
