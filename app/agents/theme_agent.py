from app.agents.base import SkillAgent


class ThemeAgent(SkillAgent):
    name = "ThemeAgent"

    def __init__(self, catalog):
        self.catalog = catalog

    def run(self, context: dict) -> dict:
        occasion = str(context.get("occasion", "general")).strip().lower()
        style_hint = str(context.get("style_hint", "minimal")).strip().lower()
        tokens = set((occasion + " " + style_hint).replace(",", " ").split())

        scored = []
        for theme in self.catalog.themes:
            searchable = set(theme.get("occasions", [])) | set(theme.get("styles", []))
            searchable |= set(str(theme.get("name", "")).lower().split())
            searchable |= set(str(theme.get("composition", "")).lower().replace("_", " ").split())
            score = len(tokens.intersection(searchable))
            scored.append((score, theme))

        scored.sort(key=lambda item: (item[0], not item[1].get("premium", False)), reverse=True)
        theme = scored[0][1]
        return {
            "agent": self.name,
            "recommended_theme": theme,
            "reason": f"Theme choisi pour occasion={occasion} et style={style_hint}.",
        }
