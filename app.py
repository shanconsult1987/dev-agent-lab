
import json
from pathlib import Path


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
STATE_FILE = DATA_DIR / "state.json"
AUDIT_FILE = DATA_DIR / "audit.jsonl"


def make_plan(request: str) -> dict:
    """Create a predictable plan for a feature request."""
    request = request.strip()

    if not request:
        raise ValueError("Feature request cannot be empty.")

    return {
        "request": request,
        "status": "planned",
        "steps": [
            "Understand the requirement",
            "Identify the smallest implementation change",
            "Add or update unit tests",
            "Run validation and request human review",
        ],
        "acceptance_criteria": [
            "The requested behavior is documented",
            "Tests cover expected behavior",
            "Validation completes successfully",
        ],
    }


def save_state(state: dict) -> None:
    """Save the latest workflow state."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8",
    )


def record_event(event: dict) -> None:
    """Append an event to the workshop audit log."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with AUDIT_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")


def main() -> None:
    request = input("Enter a feature request: ").strip()

    try:
        plan = make_plan(request)
    except ValueError as error:
        print(f"Error: {error}")
        return

    save_state(plan)
    record_event({
        "event": "plan_created",
        "request": request,
        "status": plan["status"],
    })

    print(json.dumps(plan, indent=2))
    print(f"\nState saved to: {STATE_FILE}")
    print(f"Audit log: {AUDIT_FILE}")


if __name__ == "__main__":
    main()
