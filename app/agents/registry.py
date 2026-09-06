AGENT_REGISTRY = {
    "layout": {"class": "LayoutRecommendationAgent", "max_input_tokens": 2000, "max_output_tokens": 250, "max_tool_calls": 1},
    "theme": {"class": "ThemeAgent", "max_input_tokens": 3500, "max_output_tokens": 500, "max_tool_calls": 2},
    "qa": {"class": "QAContentAgent", "max_input_tokens": 2500, "max_output_tokens": 250, "max_tool_calls": 1},
}
