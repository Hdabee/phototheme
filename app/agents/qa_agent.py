from app.agents.base import SkillAgent

REQUIRED_THEME_FIELDS = {"id", "name", "background", "premium"}


class QAContentAgent(SkillAgent):
    name = "QAContentAgent"

    def run(self, context: dict) -> dict:
        theme = context.get("recommended_theme")
        if not isinstance(theme, dict):
            return {"agent": self.name, "valid": False, "errors": ["Theme absent ou invalide."]}

        missing = sorted(REQUIRED_THEME_FIELDS.difference(theme.keys()))
        errors = []
        if missing:
            errors.append("Champs manquants: " + ", ".join(missing))
        if not isinstance(theme.get("premium"), bool):
            errors.append("premium doit etre un booleen.")
        return {"agent": self.name, "valid": not errors, "errors": errors}
