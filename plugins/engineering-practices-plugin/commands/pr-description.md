---
description: Write a pull request description for the current branch, derived from the diff
---

# Write PR Description (markdown output): $ARGUMENTS

## Objective

Produce a pull request description for the current branch, ready to paste into GitHub. Output it as
markdown in a fenced code block. Fill the repo's PR template from the actual diff — do not invent
work that isn't in the changes.

`$ARGUMENTS` is optional extra context (a ticket ID, the base branch, or what to emphasise). If
empty, infer everything from the branch and its commits.

## Process

1. Determine the base branch and gather the diff. Default to the repository's default branch unless
   `$ARGUMENTS` names another; resolve it with `git symbolic-ref --short refs/remotes/origin/HEAD`.
   - `git log --oneline <base>..HEAD` — the commits on this branch
   - `git diff --stat <base>...HEAD` — files and line counts
   - `git diff <base>...HEAD` — the actual changes, when you need detail for a section
2. Read the template at `.github/pull_request_template.md` and use its exact section headings. If
   that file is absent, use `${CLAUDE_PLUGIN_ROOT}/templates/pull_request_template.md`. If neither
   exists, fall back to the Output structure below.
3. Identify the ticket (from the branch name, a commit trailer such as `Refs ABC-123`, or
   `$ARGUMENTS`) and any ADR or spec the work references. Link them.
4. Write each section from what the diff actually shows.
5. Output the finished description as a single markdown code block so it can be copied verbatim.
   If any section contains its own fenced code block (for example test commands under Steps to
   Test), wrap the whole description in a four-backtick (````) fence so the inner triple-backtick
   blocks are preserved instead of closing the outer fence early. Do not create a file and do not
   push anything.

## Output

Match `.github/pull_request_template.md`. The default template has these sections:

```markdown
## Scope

[One or two sentences: what this PR is and, if it's part of a larger ticket, which slice. State
what is deliberately NOT in this PR when the ticket is being split.]

## Work Done

[The concrete changes, as a short list. Each item names the thing that changed and why. Reference
paths and any ADR or spec. Call out generated code, migrations, and lock files separately — they
carry review burden even when they don't count to the line budget.]

## Steps to Test

[How a reviewer verifies it. The exact commands for this project's toolchain and, for behavioural
changes, what to observe. If there is nothing to run, say what was checked and how.]

## Screenshots

[Only for user-visible output. Otherwise "N/A".]
```

If the template file differs from this snippet, follow the file.

## Rules

- Derive everything from the diff. If you cannot support a claim from the changes, do not make it.
- Note deviations from the spec or ticket, and why, if any exist. Every `feat:` PR links its spec.
- State backwards-compatibility impact when the change alters an API, wire format, or response shape.
- Keep it tight. A reviewer should grasp the PR from Scope and Work Done alone.
- Take test commands from this project's own tooling — its task runner, package scripts, or CI
  workflow. Do not assume a language or a command that the repo does not use.
- Plain language: no "lands", "wired in", "wire up", "thread through", "seam", "load-bearing",
  "ships", "in flight". Use "added to", "runs against", "consolidated onto", etc. ("wire format" is
  fine.)
- If the diff exceeds roughly 400 lines of meaningful change, say so at the end of the output and
  suggest where it could split. Do not refuse to write the description.
- If the branch has no commits beyond the base, say so instead of inventing a description.
- Do not commit, push, or open the PR — only produce the text.
