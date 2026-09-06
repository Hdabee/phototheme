from app.agents.orchestrator import AgentOrchestrator


def test_theme_workflow_returns_qa():
    result = AgentOrchestrator().run("theme_recommendation", {
        "photo_count": 4,
        "target_format": "square",
        "occasion": "anniversaire",
        "style_hint": "pastel",
        "locale": "fr-FR",
    })
    assert result["qa"]["valid"] is True
    assert result["recommended_theme"]["id"]
