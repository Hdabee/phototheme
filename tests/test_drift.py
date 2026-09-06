from app.agents.orchestrator import AgentOrchestrator


def test_theme_baseline_is_stable():
    context = {
        "photo_count": 4,
        "target_format": "story",
        "occasion": "travel",
        "style_hint": "postcard warm",
        "locale": "fr-FR",
    }
    first = AgentOrchestrator().run("theme_recommendation", context)
    second = AgentOrchestrator().run("theme_recommendation", context)
    assert first["recommended_theme"]["id"] == second["recommended_theme"]["id"]
