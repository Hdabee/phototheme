from dataclasses import asdict, dataclass

@dataclass
class ProjectStoryState:
    title: str = "UNE VIE EN QUATRE REGARDS"
    subtitle: str = "Des premiers souvenirs à aujourd'hui"
    place: str = "THEN / NOW"
    period: str = "1964 - 2026"
    hero_photo_id: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
