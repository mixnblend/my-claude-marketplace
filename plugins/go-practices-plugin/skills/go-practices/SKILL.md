---
name: go-practices
description: Worked examples and full rationale for the Go code quality, conventions, and testing rules — HTTP service structure (run, NewServer, addRoutes, handler makers), pgx database access, error handling, package layout, BDD-style testify tests, table-driven tests, integration test suites with testcontainers. Use when writing or reviewing Go code and a rule needs an example, or when setting up a new Go service, test suite, or package.
---

# Go Practices

The `go-*` rules state each convention in one line. This skill holds the examples and the reasons behind them. Read the reference file that matches the task:

| Task | Reference |
| ---- | --------- |
| Function size, naming, comments, signatures, early returns, file layout | `references/code-quality.md` |
| HTTP service structure, middleware, pgx, transactions, migrations, errors, package structure | `references/conventions.md` |
| testify assertions, Given/When/Then, table-driven tests, helpers, integration tests, mocks, suites | `references/testing.md` |

Read only the file you need. Each file is self-contained.
