
# Agent Evaluation

Evaluate each proposed plan and implementation.

| Criterion | Passing condition |
|---|---|
| Completeness | Goal, steps, and acceptance criteria are present |
| Relevance | Steps address the actual request |
| Testability | Criteria can be verified |
| Safety | No unauthorized execution is proposed |
| Traceability | Request and decision are recorded |
| Validation | Required automated checks pass |

## Failure handling

1. Record the failed criterion.
2. Identify the cause.
3. Correct the relevant prompt, context, tool, or code.
4. Rerun the same test case.
5. Confirm previously passing tests still pass.

## LLM evaluation

Use fixed feature requests for repeatable comparisons.
Validate JSON and required fields before scoring content.
Record the model, prompt version, inputs, and results.
Do not rely on a single successful response.
