class InputGuard:
    BLOCKED_TERMS = {
        "ignore previous instructions",
        "reveal secret",
        "system prompt",
    }

    def validate(self, context: dict) -> None:
        text = " ".join(str(value).lower() for value in context.values())
        if any(term in text for term in self.BLOCKED_TERMS):
            raise ValueError("Requete bloquee par le guardrail d'entree.")
        if not 2 <= int(context.get("photo_count", 0)) <= 9:
            raise ValueError("photo_count doit etre compris entre 2 et 9.")
