class OutputGuard:
    def validate_theme(self, theme: dict, qa: dict) -> None:
        if not qa.get("valid"):
            raise ValueError("Sortie theme rejetee: " + "; ".join(qa.get("errors", [])))
        if not theme.get("id"):
            raise ValueError("Sortie theme rejetee: identifiant absent.")
