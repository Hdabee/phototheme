import pytest
from app.agents.factory import SkillAgentFactory
from app.services.catalog_service import CatalogService

def test_factory_creates_theme_agent():
    agent = SkillAgentFactory(CatalogService()).create("theme")
    assert agent.name == "ThemeAgent"

def test_factory_rejects_unknown_agent():
    with pytest.raises(ValueError):
        SkillAgentFactory(CatalogService()).create("unknown")
