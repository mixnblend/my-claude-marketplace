---
name: project-documentation
description: Formatting rules, templates, and conventions for all documents in docs/. Use when producing or editing ADRs, specs, plans, or research documents. Loaded explicitly by /research, /plan, /write-spec, and /write-adr commands, and should also be consulted when editing any existing document in docs/.
---

# Project Documentation Conventions

## File Naming

| Type | Location | Command |
| ---- | -------- | ------- |
| Research | `docs/research/[NN]-[ticket-id]-[short-slug].md` | `/research` |
| Plan | `docs/plans/[NN]-[ticket-id]-[short-slug].md` | `/plan` |
| Specification | `docs/specs/[NN]-[ticket-id]-[short-slug].md` | `/write-spec` |
| ADR | `docs/adr/NNNN-[short-title].md` | `/write-adr` |

Specs, research, and plans are prefixed with a two-digit sequence number (`NN`) matching the backlog implementation order, followed by the ticket ID and a short slug. This makes the project timeline visible when browsing the directory. Look up the ticket's position in `docs/BACKLOG.md` to determine the sequence number.

Examples: `01-dev-1-justfile-asdf.md`, `03-infra-1-deployment-manifests.md`, `15-delivery-1-temporal-delivery-workflow.md`.

ADRs use a four-digit sequential number: `0001-short-title.md`. Determine the next number by checking `docs/adr/` for the highest existing number.

Slugs are lowercase, hyphen-separated, and descriptive.

## Headings

The `# heading` of each document must include the sequence number: `# 03 — Specification: Deployment Manifests`.

Use ATX headings (`#`, `##`, `###`). Do not use setext (underline) headings. Do not skip heading levels. One blank line before and after headings.

## General Formatting

- Wrap prose at a reasonable length — do not produce single-line paragraphs that span hundreds of characters.
- Use fenced code blocks with a language identifier for all code samples.
- Prefer prose over bullet lists for explanatory content. Use bullets only for genuinely list-shaped data (file inventories, checklists, enumerated options).
- Use Markdown tables for structured data — file lists, decisions, comparisons. Prefer tables over bullet lists when entries have consistent fields. Always include header row and alignment row.
- Match the formatting of existing documents in the same directory. When in doubt, check a recent example.

## Line Limits

- **Specs**: under 100 lines. If longer, the scope is probably too broad.
- **Research docs**: no hard limit, but favour relevance over exhaustiveness.
- **Plans**: under 200 lines. If longer, the work should be split into separate tasks.
- **ADRs**: under 50 lines. A good ADR is short and specific.

## Decisions Tables

### Comparing alternatives

When a document evaluates options, use a comparison table:

```markdown
| Option | Pros | Cons | Chosen |
|--------|------|------|--------|
| Option A | ... | ... | ✓ |
| Option B | ... | ... | |
```

Follow the table with a paragraph explaining why the chosen option was selected.

### Recording resolved questions

When a research document or plan has open questions that are resolved by the user, replace the "Open Questions" section with a "Decisions" section:

```markdown
## Decisions

The following questions were raised during research. Decisions are recorded here for traceability.

| # | Question | Decision |
| - | -------- | -------- |
| 1 | Short question? | **Answer.** Rationale. Note if a skill file was updated. |
| 2 | Another question? | **Answer.** Rationale. |
```

When a decision establishes a new convention, update the relevant skill file and note "Skill file updated." in the decision cell.

## ADR Format

Sections:

- **Status** — Accepted, Superseded, or Deprecated.
- **Context** — what situation prompted this decision, what constraints existed.
- **Decision** — what we decided, specific about the approach.
- **Consequences** — trade-offs, what becomes easier, what becomes harder, follow-up actions.

Rules for ADRs:

- Be specific and concrete. "We chose X because Y" beats "We evaluated several options."
- Record the context at the time of the decision.
- Include consequences honestly — every decision has trade-offs.
- Only produce an ADR for architectural decisions, new patterns, technology choices, or significant trade-offs. Not for routine feature work or bug fixes.

## Linting

After writing or editing any document in `docs/`, run:

```bash
markdownlint-cli2 --fix "**/*.md" "#vendor"
```

Then re-run without `--fix` to check for remaining issues and resolve them manually.
