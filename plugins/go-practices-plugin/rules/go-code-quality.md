---
paths:
  - "**/*.go"
---

# Go Code Quality

- Keep functions small. Each function does one thing at one level of abstraction. If a block needs a comment to say what it does, extract it into a function whose name replaces the comment.
- Choose names that state intent: `decodeDeliveryInstruction`, not `proc`; `retryCountByProvider`, not `m`. Short names are fine for receivers and for loop variables in small scopes.
- Comments explain why, not what. Comment non-obvious decisions, workarounds (link the issue), and chosen values. Write godoc only when the name and signature do not already say it.
- Do not write grouping comments or section dividers (`// Error cases`, `// --- helpers ---`). Use well-named variables or separate functions instead.
- If a function takes more than 3–4 parameters, group them into a struct or split the function.
- Use early returns for errors and edge cases. Keep the main logic at the lowest indentation level.
- Organise files by concern, not by kind: `item.go`, `store.go`, `item_test.go`. No `models.go`, `interfaces.go`, or `errors.go`.
- Sentinel errors live in the file that defines the type they relate to.

For examples, load the `go-practices` skill and read `references/code-quality.md`.
