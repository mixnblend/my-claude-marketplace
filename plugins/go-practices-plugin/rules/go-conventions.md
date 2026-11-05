---
paths:
  - "**/*.go"
---

# Go Conventions

## Standard library first

- HTTP routing: `net/http` with Go 1.22+ `ServeMux` patterns. Not chi, gorilla, or fiber.
- Logging: `log/slog`. Not zerolog, zap, or logrus.
- JSON: `encoding/json`, unless profiling shows a bottleneck.
- `context.Context` is the first parameter of every function that does I/O.

## HTTP services

- `main()` only calls `run(ctx, args, getenv, stdout, stderr) error`. Pass OS values in; do not read them globally.
- `NewServer(...)` takes every dependency as an explicit argument and returns `http.Handler`.
- `addRoutes` in `routes.go` lists the full API surface, with middleware applied inline.
- Handlers are maker functions that return `http.Handler`, not methods on a server struct. Define request and response types inside the maker when only it uses them.
- Use one generic `encode`/`decode` helper pair for JSON.
- Validate locally checkable things only. Use `go-playground/validator` struct tags, or a `Valid(ctx) map[string]string` method.
- Middleware is `func(http.Handler) http.Handler`.
- Always shut down gracefully: `signal.NotifyContext` in `run`, and a `WaitGroup` to drain.
- Defer expensive handler setup with `sync.Once`.

## Database

- Use `pgx` with SQL strings, `pgx.NamedArgs`, and the `pkg/database/v1/` pool wrapper. No ORMs. Do not use a raw pool.
- Use the `WithTx(ctx, pool, fn)` helper for transactions. Do not call `Begin`/`Commit`/`Rollback` by hand.
- Migrations: `pressly/goose/v3` in `cmd/<service>/migrations/*.sql`, embedded with `//go:embed`.
- DB-backed services add `pool.Ping(ctx)` to `/healthz`. No separate readiness probe.

## Errors, constructors, state

- Define sentinel errors for known failures. Wrap with `fmt.Errorf("doing x: %w", err)`.
- Use functional options when a constructor has more than two optional parameters. Prefer explicit arguments over a config struct for long dependency lists.
- The only package-level variables are sentinel errors. No global pools or loggers.

## Packages

- Name packages for what they contain. Never create `service/`, `repository/`, `ports/`, `adapters/`, `driven/`, `driving/`, `utils/`, or `helpers/`. `internal/domain/` is allowed for a shared aggregate root and its events.
- Define interfaces at the consumer, and only when something must mock or swap the implementation.
- No service layer that only delegates to a store. No DTOs that mirror domain structs field for field.

## Infrastructure

- Terraform for infrastructure, Helm charts in `deploy/`, multi-stage Docker builds with a non-root user.

For examples, load the `go-practices` skill and read `references/conventions.md`.
