
# Development Practices

These practices apply to all development work regardless of language or project.

## Commits

Use conventional commits for all commit messages: `type(scope): description`.

Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `ci`.

There is no `test` type. Test-only changes use `chore`.

Scope is the package, module, or area of change. Keep descriptions concise and in imperative mood.

Use only these types: `feat`, `fix`, `refactor`, `chore`, `docs`, `ci`.

```text
feat(delivery): add retry logic for transient provider failures
fix(item): handle duplicate message IDs in event consumer
refactor(stock): extract validation into domain type
chore(deps): bump pgx to v5.7.2
chore(delivery): add integration tests for provider timeout
docs(adr): record decision to remove SVIX
ci(pipeline): add PR size warning check
```

Each commit should represent a single coherent change. Do not bundle unrelated changes in one commit.

## Pull Request Discipline

### Size

Keep pull requests to roughly 400 lines of meaningful change. This is a guideline, not a hard rule — a 500-line PR with clear intent is fine, a 1200-line PR needs splitting.

If a task produces more than 400 lines, split it into multiple PRs that each make sense independently. Each PR should leave the codebase in a working state.

Generated code, migrations, and lock files don't count towards the line budget in the same way as hand-written logic, but they still add review burden — call them out in the PR description.

### Spec-Linked Delivery

Every `feat:` PR must link to its specification in `docs/specs/`. The PR description should include:

- What spec it implements
- Any deviations from the spec discovered during implementation
- Why the deviation was necessary

If there is no spec for the work, write one first (`/write-spec`). Specs don't need to be long — a 30-line spec that captures the problem, approach, and testing strategy is enough.

### The Litmus Test

Before opening a PR, ask: **"Can I explain every change in this PR to a colleague?"**

If you can't, the PR is either too large, doing too many things, or contains changes you don't fully understand. In any of those cases, stop and address the issue before requesting review.

This applies equally to human-written and agent-generated code. Understanding what you're shipping is non-negotiable.

## Architecture Decision Records

Produce an ADR (`docs/adr/NNNN-short-title.md`) when:

- Introducing a new pattern or technology
- Making a significant trade-off between approaches
- Changing an established convention
- Deciding against a commonly expected approach

Do not produce an ADR for bug fixes, minor refactors, or routine feature work that follows existing patterns.

## Definition of Done

Before reporting any task as complete:

- All TODO/FIXME items removed or captured in tickets
- All tests passing — unit, integration, clean
- Linters and formatters clean
- Documentation updated (ADR if applicable, spec updated if implementation diverged)
- Edge cases from the plan actually handled
- Backwards-compatibility implications considered
- Commit messages follow conventional commit format
- PR is under ~400 lines of meaningful change (split if not)
- `feat:` PRs link to their spec
- You can explain every change in the PR to a colleague
