---
name: specification
description: Protocol for writing a specification document that captures the problem, approach, and constraints for a piece of work. Use when a task needs a spec before research and planning can begin.
---

# Specification Protocol

## Process

1. Understand the task described in the arguments.
2. If existing code or documentation is relevant, read it to understand current state.
3. Draft the specification following the output format below.
4. Flag any ambiguities or open questions — do not make assumptions silently.

## Output

Create `docs/specs/[ticket-id]-[short-slug].md` (e.g. `infra-1-deployment-manifests.md`).

Frontmatter: `Status: Draft`, `Date: [today]`, `Author: [name]`.

Sections:

- **Problem Statement** — what problem are we solving, why it matters, current behaviour vs desired behaviour.
- **Proposed Approach** — how we intend to solve this, at a level of detail sufficient for planning (not implementation). Include enough domain context for someone unfamiliar with this area to understand the reasoning.
- **Files Affected** — which packages and files will change, which new files will be created. Doesn't need to be exhaustive but should capture the major areas.
- **Testing Strategy** — what needs to be tested, what types of tests (unit, integration), existing test patterns to follow.
- **Verification** — how do we know this is working correctly, what can be checked manually or automatically.
- **Rollback Considerations** — what happens if this needs to be reverted, any irreversible steps (migrations, data changes, external system interactions).
- **Open Questions** — anything that needs human input or further investigation before implementation.

## Rules

- Write for clarity, not completeness. A 50-line spec that captures the key decisions is better than a 200-line spec that covers every edge case.
- Do not describe implementation details (specific function signatures, exact SQL queries). Describe what needs to happen and why.
- If you're unsure about the right approach, describe the options and their trade-offs in the open questions section rather than picking one silently.
- The spec should be understandable by someone who knows the domain but hasn't looked at this specific area of the codebase recently.
- Follow the formatting rules in the project-documentation skill.
