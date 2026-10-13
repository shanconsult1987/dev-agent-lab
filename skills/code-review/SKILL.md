
---
name: code-review
description: Review small code changes against requirements, tests, and safety rules.
---

# Code Review Skill

When reviewing a proposed change:

1. Read docs/specs.md.
2. Identify the linked issue and its acceptance criteria.
3. Inspect the complete diff.
4. Check input validation and error handling.
5. Check whether tests cover valid and invalid inputs.
6. Look for exposed secrets and unsafe execution.
7. Report findings with file references where possible.
8. Return PASS or FAIL with a short explanation.

Never approve or merge a pull request automatically.
Never claim a test passed without validation evidence.
