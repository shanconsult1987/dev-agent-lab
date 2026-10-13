
import json
import os

from openai import OpenAI


def create_llm_plan(request: str) -> dict:
    """Ask an OpenAI model for a structured development plan."""
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
            "Return valid JSON with exactly these required fields: "
            "summary, steps, acceptance_criteria, risks. "
            "The last three fields must be arrays of strings. "
            "Do not claim that code has been modified."
        ),
        input=request,
    )

    try:
        result = json.loads(response.output_text)
    except json.JSONDecodeError as error:
        raise ValueError("The model did not return valid JSON.") from error

    if not isinstance(result, dict):
        raise ValueError("The model response must be a JSON object.")

    required = {
        "summary",
        "steps",
        "acceptance_criteria",
        "risks",
    }

    if not required.issubset(result):
        raise ValueError("The model response is missing required fields.")

    for field in ("summary",):
        if not isinstance(result[field], str):
            raise ValueError(f"{field} must be a string.")

    for field in ("steps", "acceptance_criteria", "risks"):
        if not isinstance(result[field], list):
            raise ValueError(f"{field} must be a list.")

        if not all(isinstance(item, str) for item in result[field]):
            raise ValueError(f"Every item in {field} must be a string.")

    return result


if __name__ == "__main__":
    feature = input("Feature request: ")
    print(json.dumps(create_llm_plan(feature), indent=2))
