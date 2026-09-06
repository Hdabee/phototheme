from app.agents.factory import SkillAgentFactory
from app.agents.registry import AGENT_REGISTRY
from app.guardrails.budget_guard import BudgetGuard
from app.guardrails.input_guard import InputGuard
from app.guardrails.output_guard import OutputGuard
from app.services.catalog_service import CatalogService
from app.services.trace_service import TraceService

class AgentOrchestrator:
    def __init__(self):
        self.catalog = CatalogService()
        self.factory = SkillAgentFactory(self.catalog)
        self.input_guard = InputGuard()
        self.output_guard = OutputGuard()
        self.trace = TraceService()

    def available_agents(self) -> list[str]:
        return list(AGENT_REGISTRY.keys())

    def run(self, intent: str, context: dict) -> dict:
        self.input_guard.validate(context)
        if intent == "layout_recommendation":
            result = self._run_agent("layout", context)
        elif intent == "theme_recommendation":
            result = self._run_theme_workflow(context)
        elif intent == "creative_workflow":
            layout = self._run_agent("layout", context)
            theme = self._run_theme_workflow(context)
            result = {"layout": layout, "theme": theme}
        else:
            raise ValueError(f"Intent non pris en charge: {intent}")
        self.trace.write(intent, context, result)
        return result

    def _run_theme_workflow(self, context: dict) -> dict:
        theme_result = self._run_agent("theme", context)
        qa_context = {**context, **theme_result}
        qa_result = self._run_agent("qa", qa_context)
        self.output_guard.validate_theme(theme_result["recommended_theme"], qa_result)
        return {**theme_result, "qa": qa_result}

    def _run_agent(self, agent_type: str, context: dict) -> dict:
        guard = BudgetGuard(AGENT_REGISTRY[agent_type])
        guard.check_context(context)
        agent = self.factory.create(agent_type)
        result = agent.run(context)
        guard.check_result(result)
        result["budget"] = guard.snapshot()
        return result
