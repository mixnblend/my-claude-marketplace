---
name: implementation-phase
description: Protocol for executing an approved implementation plan phase by phase. Use when implementing a plan from docs/plans/ that has been reviewed and approved by a human.
---

# Implementation Phase Protocol

The plan has been reviewed and approved. Follow it.

## Phase Execution

For each phase in the plan:

1. Read the phase description and understand what needs to change.
2. Implement the changes described.
3. Write the tests described.
4. Verify:
   - `go vet ./...`
   - `golangci-lint run`
   - `go test ./...`
   - `go test -tags=integration ./...` (integration tests use build tags and are not included in a plain `go test ./...` — both must pass)
   - `gofumpt` applied to all modified files
5. Confirm the phase's verification steps pass.
6. Update the plan file with the phase status (mark as complete, note any deviations).
7. Commit the phase before moving on. Each phase gets its own commit so the history is bisectable and phases can be reviewed independently.
8. Compact context before starting the next phase.

## Rules

- Follow the plan. If you discover something that requires deviating, stop and describe what you found. Do not silently change approach.
- Commit format, PR discipline, and definition of done are defined in `.claude/rules/development-practices.md` — follow them.
- Compact between phases. Do not carry the full context of phase 1 into phase 3.
- Run linting and tests after each phase, not just at the end.
- If tests fail, fix them in the current phase. Do not move on with broken tests.
- Any deviations from the plan must be documented in the plan file.
