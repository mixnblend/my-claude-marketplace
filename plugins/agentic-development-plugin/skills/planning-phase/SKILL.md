---
name: planning-phase
description: Protocol for producing a phased implementation plan from a research document. Use when breaking down a task into implementable phases after research is complete.
---

# Planning Phase Protocol

Do not write any implementation code during planning.

## Process

1. Review the research document in `docs/research/` — it describes what exists and what needs to change.
2. Review the specification in `docs/specs/` if one exists.
3. Break the work into phases. Each phase should be:
   - A coherent unit of work that can be implemented and verified independently
   - Small enough to review in a single session (aim for under 400 lines of change per phase)
   - Ordered so that each phase builds on the previous one
4. For each phase, specify exactly what changes, what tests to write, and how to verify it works.

## Output

Produce `docs/plans/[task-slug].md` with these sections:

- **Summary** — one paragraph describing the overall approach.
- **Phases** — each phase includes:
  - What changes (files, packages, and why)
  - What tests to write
  - Verification steps to confirm the phase is correct before moving on
- **Testing Strategy** — overall approach to testing this change.
- **Rollback Considerations** — what happens if we need to revert, any irreversible steps.
- **Open Questions** — anything that came up during planning that needs human input.

## Rules

- Do not write implementation code — describe what needs to happen, not how to write it.
- Each phase must be independently verifiable. Do not create phases that only make sense when combined with the next one.
- If the plan would require deviating from conventions in CLAUDE.md, flag it explicitly.
- If the research document has open questions that affect the plan, list them and explain what the plan assumes.
- Keep the plan under 200 lines. If it's longer, the work should probably be split into separate tasks.
- Follow the formatting rules in `${CLAUDE_PLUGIN_ROOT}/rules/project-documentation.md`.
