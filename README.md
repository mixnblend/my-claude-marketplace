# My Claude Code Plugin Marketplace

A personal collection of Claude Code plugins for Go development, engineering practices, and agentic workflows.

## Installation

Add the marketplace, then install a plugin from it:

```bash
/plugin marketplace add mixnblend/my-claude-marketplace
/plugin install <plugin-name>@my-plugins
```

The marketplace is named `my-plugins` — that is the `name` field in `.claude-plugin/marketplace.json`, not the repository name. Use `my-plugins` after the `@`.

To pick up new or changed plugins after this repository is updated:

```bash
/plugin marketplace update my-plugins
/plugin update <plugin-name>@my-plugins
```

Updating the marketplace refreshes the catalogue; it does not update a plugin that is already installed. Restart Claude Code afterwards so new commands and skills load.

## Installing Rules

Claude Code does not load a plugin's `rules/` directory. Two rules load through a `SessionStart` hook instead, so they work as soon as you install the plugin:

| Rule | Plugin |
| ---- | ------ |
| `development-practices` | `engineering-practices-plugin` |
| `simplified-technical-english` | `technical-writing-plugin` |

Do not copy these two rules as well. If you do, Claude loads them twice.

The other rules are path-scoped, and a hook cannot scope them. To use them, copy them into a rules directory:

| Destination | Effect |
| ----------- | ------ |
| `~/.claude/rules/` | The rules apply in every project |
| `<project>/.claude/rules/` | The rules apply in that project only. Commit them to share them with the team |

```bash
git clone https://github.com/mixnblend/my-claude-marketplace.git
mkdir -p ~/.claude/rules
cp my-claude-marketplace/plugins/go-practices-plugin/rules/*.md ~/.claude/rules/
cp my-claude-marketplace/plugins/agentic-development-plugin/rules/*.md ~/.claude/rules/
```

A rule without `paths` front matter loads at the start of every session. A rule with `paths` loads only when Claude works on a matching file. Run `/context all` to see which rules loaded.

Copied rules do not update with the plugin. Copy them again after you pull changes.

## Hooks

Hooks run automatically when the plugin is installed. A rule is guidance that Claude can miss; a hook runs every time.

| Plugin | Event | What it does | Needs |
| ------ | ----- | ------------ | ----- |
| `engineering-practices-plugin` | `SessionStart` | Loads the `development-practices` rule | — |
| `technical-writing-plugin` | `SessionStart` | Loads the `simplified-technical-english` rule | — |
| `go-practices-plugin` | `PostToolUse` on `Edit\|Write` | Reports `gofmt` and `go vet` problems in the edited file's package | `go`, `jq` |
| `agentic-development-plugin` | `PostToolUse` on `Edit\|Write` | Reports `markdownlint-cli2` problems in an edited Markdown file under `docs/` | `markdownlint-cli2`, `jq` |

The hooks report problems to Claude. They do not change files. A hook skips silently when a tool it needs is not installed.

## Plugins

### go-practices-plugin

Opinionated Go rules covering code quality, conventions, and testing. The rules are short, one line per convention. The `go-practices` skill holds the worked examples, so they load only when needed.

**Rules** (copy into a rules directory — see [Installing Rules](#installing-rules)):

| Rule | Scope | Description |
|------|-------|-------------|
| `go-code-quality` | `**/*.go` | Small functions, naming, comments, early returns, package organisation |
| `go-conventions` | `**/*.go` | Standard library-first HTTP services, pgx database access, error handling, package structure |
| `go-testing` | `**/*_test.go` | BDD-style tests with testify, table-driven tests, integration test suites, mocking conventions |

**Skills:**

| Skill | Description |
|-------|-------------|
| `go-practices` | Worked examples and rationale for every Go rule, split into code quality, conventions, and testing references |

### engineering-practices-plugin

Language-agnostic engineering practices that apply to all development work.

**Rules** (loaded by a hook — see [Hooks](#hooks)):

| Rule | Description |
|------|-------------|
| `development-practices` | Conventional commits, PR discipline (~400 lines), spec-linked delivery, ADRs, definition of done |

**Commands:**

| Command | Description |
|---------|-------------|
| `/pr-description` | Write a PR description for the current branch, derived from the diff, filling the repo's PR template |

**Templates:**

`templates/pull_request_template.md` is a language-agnostic PR template with Scope, Work Done, Steps to Test, and Screenshots sections. `/pr-description` falls back to it when a repo has no `.github/pull_request_template.md`. Copy it into a repo to adopt it:

```bash
cp plugins/engineering-practices-plugin/templates/pull_request_template.md .github/
```

`templates/.commitlintrc.json` is a [commitlint](https://commitlint.js.org/) config that enforces the commit format from the `development-practices` rule. It allows only the types `feat`, `fix`, `refactor`, `chore`, `docs`, and `ci`. The rule tells Claude the format; commitlint rejects commits that break it, from Claude and from people. Install it in a repo as a git `commit-msg` hook:

```bash
cp plugins/engineering-practices-plugin/templates/.commitlintrc.json .
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky
npx husky init
echo 'npx --no -- commitlint --edit "$1"' > .husky/commit-msg
```

`npx husky init` also writes a `.husky/pre-commit` file that runs `npm test`. Delete it or edit it if the repo does not use `npm test`. Any git hook manager works in place of husky, for example lefthook. The `commit-msg` hook must run `npx --no -- commitlint --edit <message-file>`.

### agentic-development-plugin

A phased, human-in-the-loop development workflow inspired by the spec-research-plan-implement pattern.

**Commands:**

| Command | Description |
|---------|-------------|
| `/spec` | Write a specification document capturing the problem, approach, and constraints |
| `/research` | Investigate the codebase without writing code; produce a research document |
| `/plan` | Produce a phased implementation plan from the research document |
| `/implement` | Execute an approved plan phase by phase |
| `/adr` | Write an Architecture Decision Record for completed work |

**Rules** (copy into a rules directory — see [Installing Rules](#installing-rules)):

| Rule | Scope | Description |
|------|-------|-------------|
| `project-documentation` | `docs/**` | File naming, headings, line limits, decision tables, and ADR format for all documents in `docs/`. The commands read it directly, so they work without copying it |

This plugin uses the `development-practices` rule from `engineering-practices-plugin`.

**Skills:**

| Skill | Description |
|-------|-------------|
| `specification` | Protocol for writing spec documents |
| `research-phase` | Protocol for codebase investigation before planning |
| `planning-phase` | Protocol for breaking work into implementable phases |
| `implementation-phase` | Protocol for executing approved plans |

### technical-writing-plugin

Applies ASD-STE100 Simplified Technical English discipline to technical documentation: one meaning per word, active voice, simple tenses, short sentences, no ellipsis. The rule applies the core constraints whenever Claude writes documentation, commit messages, or error strings. The commands and skill do a full rewrite or review on request.

**Rules** (loaded by a hook — see [Hooks](#hooks)):

| Rule | Description |
|------|-------------|
| `simplified-technical-english` | Core STE constraints: one meaning per word, active voice, simple tenses, sentence limits, conditions first |

**Commands:**

| Command | Description |
|---------|-------------|
| `/ste` | Rewrite a document, section, or pasted text into Simplified Technical English |
| `/ste-review` | Report which rules a document breaks, without editing it |

**Skills:**

| Skill | Description |
|-------|-------------|
| `simplified-technical-english` | Rewrite rules, per-document-type limits, worked before/after examples |

## Repository Structure

```
.claude-plugin/
  marketplace.json        # Marketplace manifest listing all plugins
plugins/
  go-practices-plugin/
    .claude-plugin/
      plugin.json
    hooks/
    rules/
    skills/
  engineering-practices-plugin/
    .claude-plugin/
      plugin.json
    hooks/
    commands/
    rules/
    templates/
  agentic-development-plugin/
    .claude-plugin/
      plugin.json
    hooks/
    commands/
    rules/
    skills/
  technical-writing-plugin/
    .claude-plugin/
      plugin.json
    hooks/
    commands/
    rules/
    skills/
```
