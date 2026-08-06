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

## Plugins

### go-practices-plugin

Opinionated Go rules covering code quality, conventions, and testing. Activates automatically on `.go` and `_test.go` files.

**Rules:**

| Rule | Scope | Description |
|------|-------|-------------|
| `go-code-quality` | `**/*.go` | Small functions, naming, comments, early returns, package organisation |
| `go-conventions` | `**/*.go` | Standard library-first HTTP services, pgx database access, error handling, package structure |
| `go-testing` | `**/*_test.go` | BDD-style tests with testify, table-driven tests, integration test suites, mocking conventions |

### engineering-practices-plugin

Language-agnostic engineering practices that apply to all development work.

**Rules:**

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

**Skills:**

| Skill | Description |
|-------|-------------|
| `specification` | Protocol for writing spec documents |
| `research-phase` | Protocol for codebase investigation before planning |
| `planning-phase` | Protocol for breaking work into implementable phases |
| `implementation-phase` | Protocol for executing approved plans |
| `project-documentation` | Formatting rules and templates for all docs |

### technical-writing-plugin

Applies ASD-STE100 Simplified Technical English discipline to technical documentation: one meaning per word, active voice, simple tenses, short sentences, no ellipsis. Invoked explicitly — it does not activate automatically.

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
    rules/
  engineering-practices-plugin/
    .claude-plugin/
      plugin.json
    commands/
    rules/
    templates/
  agentic-development-plugin/
    .claude-plugin/
      plugin.json
    commands/
    rules/
    skills/
  technical-writing-plugin/
    .claude-plugin/
      plugin.json
    commands/
    skills/
```
