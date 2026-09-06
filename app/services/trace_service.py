import json
from datetime import datetime, timezone
from pathlib import Path

class TraceService:
    def __init__(self):
        self.path = Path(__file__).resolve().parents[2] / "data" / "traces.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, intent: str, context: dict, result: dict) -> None:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "intent": intent,
            "context": context,
            "result": result,
        }
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")
