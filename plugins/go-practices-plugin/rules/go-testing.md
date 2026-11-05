---
paths:
  - "**/*_test.go"
---

# Go Testing

- Use testify. `require` for preconditions and checks whose failure makes later checks meaningless; `assert` for the assertions under test.
- Structure every test with `// Given ...`, `// When ...`, `// Then ...` comments, with descriptive text after the ellipsis. Use `// And ...` for a further distinct step.
- Use table-driven tests for the same behaviour with varying inputs. Do not wrap a single case in a table. Write separate functions when setup or assertions differ a lot.
- Do not label groups of table rows with comments. Put each group in a well-named slice and join them with `slices.Concat`.
- Build test data with descriptive helpers that call `t.Helper()` (`validItem(t)`, `itemWithStatus(t, s)`). No generic builder chains.
- Integration tests: files end in `_integration_test.go`, functions start with `TestIntegration_`, files carry `//go:build integration`, and tests skip under `testing.Short()`. Use testcontainers.
- Prefer end-to-end HTTP tests that start the program through `run`.
- Mocks use `testify/mock`, defined in the test file that needs them (or `mocks_test.go` when shared). Call `AssertExpectations(t)`.
- Prefer `assert.Equal` over `assert.True(a == b)`. Check sentinel errors with `ErrorIs`, not string matching.
- Use `testify/suite` only for integration tests that share containers. Postgres: `Snapshot` in `SetupSuite`, `Restore` and a new pool in `SetupTest`. Kafka: a unique topic per test method.
- Before committing, run `go vet ./...`, `go test ./...`, and `go test -tags=integration ./...`. Do not commit code that breaks tests.

For examples, load the `go-practices` skill and read `references/testing.md`.
