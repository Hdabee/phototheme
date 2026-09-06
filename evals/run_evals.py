import json
from pathlib import Path
from app.agents.orchestrator import AgentOrchestrator

def main() -> None:
    scenarios = json.loads((Path(__file__).parent / "scenarios.json").read_text(encoding="utf-8"))
    orchestrator = AgentOrchestrator()
    passed = 0
    for scenario in scenarios:
        result = orchestrator.run(scenario["intent"], scenario["input"])
        if "expected_theme_id" in scenario:
            actual = result["recommended_theme"]["id"]
            expected = scenario["expected_theme_id"]
        else:
            actual = result["recommended_layouts"][0]["id"]
            expected = scenario["expected_layout_id"]
        ok = actual == expected
        passed += int(ok)
        print(f"{scenario['id']}: {'PASS' if ok else 'FAIL'} (expected={expected}, actual={actual})")
    print(f"{passed}/{len(scenarios)} scenarios passed")
    if passed != len(scenarios):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
