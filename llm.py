
import json
import os

from openai import OpenAI


def create_llm_plan(request: str) -> dict:
    if not request.strip():
        raise ValueError("Feature request cannot be empty.")

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY before using the LLM.")

    model = os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError("Set OPENAI_MODEL to an available model.")

    client = OpenAI()

    response = client.responses.create(
        model=model,
        instructions=(
            "You are a software planning agent. "
            "Do not claim that code has been changed."
        ),
        input=request,
        text={
            "format": {
                "type": "json_schema",
                "name": "software_plan",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "steps": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "acceptance_criteria": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "risks": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": [
                        "summary",
                        "steps",
                        "acceptance_criteria",
                        "risks",
                    ],
                    "additionalProperties": False,
                },
            }
        },
    )

    output_text = response.output_text.strip()
    if not output_text:
        details = response.incomplete_details
        detail_text = f" Details: {details}" if details else ""
        raise RuntimeError(f"The LLM returned no text.{detail_text}")

    try:
        result = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise ValueError("The LLM returned invalid JSON.") from exc

    required = {
        "summary",
        "steps",
        "acceptance_criteria",
        "risks",
    }

    if not isinstance(result, dict) or not required.issubset(result):
        raise ValueError("The LLM returned an invalid plan structure.")

    for key in ("steps", "acceptance_criteria", "risks"):
        if not isinstance(result[key], list) or not all(
            isinstance(item, str) for item in result[key]
        ):
            raise ValueError(f"Invalid list field: {key}")

    return result


if __name__ == "__main__":
    feature = input("Feature request: ")
    print(json.dumps(create_llm_plan(feature), indent=2))
