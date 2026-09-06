from pathlib import Path
from app.editor.photo_state import PhotoEditState
from app.editor.project_story import ProjectStoryState

class SessionStore:
    def __init__(self):
        self.sessions: dict[str, list[PhotoEditState]] = {}
        self.stories: dict[str, ProjectStoryState] = {}

    def create(self, session_id: str, paths: list[Path]) -> list[PhotoEditState]:
        states = [PhotoEditState(photo_id=f"photo_{index}", source_path=str(path)) for index, path in enumerate(paths)]
        self.sessions[session_id] = states
        self.stories[session_id] = ProjectStoryState(hero_photo_id=states[-1].photo_id if states else "")
        return states

    def get(self, session_id: str) -> list[PhotoEditState]:
        if session_id not in self.sessions:
            raise ValueError("Session introuvable ou expiree.")
        return self.sessions[session_id]

    def get_story(self, session_id: str) -> ProjectStoryState:
        if session_id not in self.stories:
            raise ValueError("Histoire introuvable ou expiree.")
        return self.stories[session_id]

    def update_story(self, session_id: str, data: dict) -> ProjectStoryState:
        story = self.get_story(session_id)
        allowed = {"title", "subtitle", "place", "period", "hero_photo_id"}
        for key, value in data.items():
            if key in allowed:
                setattr(story, key, str(value)[:90])
        if story.hero_photo_id not in {item.photo_id for item in self.get(session_id)}:
            story.hero_photo_id = self.get(session_id)[-1].photo_id
        return story

    def update(self, session_id: str, photo_id: str, data: dict) -> PhotoEditState:
        state = next((item for item in self.get(session_id) if item.photo_id == photo_id), None)
        if not state:
            raise ValueError("Photo introuvable dans cette session.")
        allowed = {"fit_mode", "rotation", "flip_horizontal", "brightness", "contrast", "saturation", "sharpness", "crop_x", "crop_y", "crop_width", "crop_height", "caption"}
        for key, value in data.items():
            if key in allowed:
                setattr(state, key, value)
        state.fit_mode = state.fit_mode if state.fit_mode in {"contain", "cover"} else "contain"
        state.rotation = int(state.rotation) % 360
        state.flip_horizontal = bool(state.flip_horizontal)
        state.caption = str(state.caption)[:40]
        for key in ("brightness", "contrast", "saturation", "sharpness"):
            setattr(state, key, max(0.2, min(2.0, float(getattr(state, key)))))
        state.crop_x = max(0.0, min(0.98, float(state.crop_x)))
        state.crop_y = max(0.0, min(0.98, float(state.crop_y)))
        state.crop_width = max(0.02, min(1.0 - state.crop_x, float(state.crop_width)))
        state.crop_height = max(0.02, min(1.0 - state.crop_y, float(state.crop_height)))
        return state

    def split_three_vertical(self, session_id: str, photo_id: str) -> list[PhotoEditState]:
        states = self.get(session_id)
        source = next((item for item in states if item.photo_id == photo_id), None)
        if not source:
            raise ValueError("Photo source introuvable.")
        position = states.index(source)
        width = source.crop_width / 3
        children = []
        for index in range(3):
            child = PhotoEditState(
                photo_id=f"{source.photo_id}_part_{index + 1}", source_path=source.source_path,
                crop_x=source.crop_x + index * width, crop_y=source.crop_y,
                crop_width=width, crop_height=source.crop_height, fit_mode="contain",
                caption=("Enfance" if index == 0 else "Jeune adulte" if index == 1 else "Portrait"),
            )
            children.append(child)
        states[position:position + 1] = children
        story = self.get_story(session_id)
        if story.hero_photo_id == photo_id:
            story.hero_photo_id = children[-1].photo_id
        return children

session_store = SessionStore()
