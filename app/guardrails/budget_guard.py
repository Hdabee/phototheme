class BudgetGuard:
    def __init__(self, config: dict):
        self.config = config
        self.input_tokens = 0
        self.output_tokens = 0
        self.tool_calls = 0

    def check_context(self, context: dict) -> None:
        self.input_tokens = max(1, len(str(context)) // 4)
        if self.input_tokens > self.config["max_input_tokens"]:
            raise ValueError("Budget input tokens depasse.")

    def check_result(self, result: dict) -> None:
        self.output_tokens = max(1, len(str(result)) // 4)
        if self.output_tokens > self.config["max_output_tokens"]:
            raise ValueError("Budget output tokens depasse.")

    def snapshot(self) -> dict:
        return {
            "mode": "simulated",
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "max_input_tokens": self.config["max_input_tokens"],
            "max_output_tokens": self.config["max_output_tokens"],
            "tool_calls": self.tool_calls,
            "max_tool_calls": self.config["max_tool_calls"],
        }
