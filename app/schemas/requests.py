from typing import Literal
from pydantic import BaseModel, Field

class LayoutRequest(BaseModel):
    photo_count: int = Field(ge=2, le=9)
    target_format: Literal["square", "story", "landscape"] = "square"
    occasion: str = Field(default="general", max_length=60)

class ThemeRequest(LayoutRequest):
    style_hint: str = Field(default="minimal", max_length=80)
    locale: str = Field(default="fr-FR", max_length=12)

class WorkflowRequest(ThemeRequest):
    request_id: str = Field(default="local-demo", max_length=80)
