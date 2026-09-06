from app.agents.layout_agent import LayoutRecommendationAgent
from app.agents.qa_agent import QAContentAgent
from app.agents.registry import AGENT_REGISTRY
from app.agents.theme_agent import ThemeAgent

class SkillAgentFactory:
    def __init__(self, catalog):
        self.catalog = catalog

    def create(self, agent_type: str):
        if agent_type not in AGENT_REGISTRY:
            raise ValueError(f"Agent non autorise: {agent_type}")
        if agent_type == "layout":
            return LayoutRecommendationAgent(self.catalog)
        if agent_type == "theme":
            return ThemeAgent(self.catalog)
        if agent_type == "qa":
            return QAContentAgent()
        raise ValueError(f"Agent sans implementation: {agent_type}")
