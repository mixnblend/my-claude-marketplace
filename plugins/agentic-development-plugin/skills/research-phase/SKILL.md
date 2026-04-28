---
name: research-phase
description: Protocol for conducting a research phase before planning or implementation. Use when starting investigation of a new task, exploring an unfamiliar area of the codebase, or when asked to research before writing code.
---

# Research Phase Protocol

Do not write any code during research.

## Process

1. Read the relevant specification in `docs/specs/` if one exists.
2. Read relevant ADRs in `docs/adr/` to understand prior decisions.
3. Explore the codebase to understand:
   - Which packages and files are involved
   - How similar functionality is currently implemented
   - What patterns and conventions are used in the relevant areas
   - What the data flow looks like (HTTP → handler → store → DB, or Kafka → consumer → processor → store)
   - What tests exist for the relevant areas
4. Identify any dependencies, edge cases, or risks.

Keep context usage minimal — use subagents for exploring large directories or reading many files.

## Output

Produce `docs/research/[task-slug].md` with these sections:

- **Summary** — one paragraph describing what you found.
- **Relevant Files** — every file that will need to change or is relevant context, with a brief note on why.
- **Current Behaviour** — how the system currently works in the relevant area.
- **Conventions Observed** — patterns used in the existing code that the implementation should follow.
- **Dependencies and Risks** — anything that could complicate implementation (cross-cutting concerns, migration needs, backwards compatibility).
- **Open Questions** — things that need human input before planning can proceed.

## Rules

- Do not write any implementation code.
- Do not make assumptions about the right approach — document what you find and flag uncertainties.
- If you find something that contradicts the specification, flag it clearly rather than resolving it yourself.
- Follow the formatting rules in the project-documentation skill.
