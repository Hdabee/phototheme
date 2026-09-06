from app.agents.base import SkillAgent

class LayoutRecommendationAgent(SkillAgent):
    name = "LayoutRecommendationAgent"

    def __init__(self, catalog):
        self.catalog = catalog

    def run(self, context: dict) -> dict:
        photo_count = context["photo_count"]
        target_format = context["target_format"]
        matches = [item for item in self.catalog.layouts if item["photo_count"] == photo_count and target_format in item["formats"]]
        if not matches:
            matches = [item for item in self.catalog.layouts if item["photo_count"] == photo_count]
        if not matches:
            raise ValueError(f"Aucun layout disponible pour {photo_count} photos.")
        return {"agent": self.name, "recommended_layouts": matches[:3], "reason": f"Layouts compatibles avec {photo_count} photos au format {target_format}."}
