---
paths:
  - "**/*.go"
---

# Go Conventions

These conventions apply to all Go code in this project. Follow them when writing new code and when modifying existing code.

## Standard Library First

Use the Go standard library wherever possible:

- `net/http` with Go 1.22+ `ServeMux` pattern matching for HTTP routing. Not chi, gorilla, or fiber.
- `log/slog` for structured logging. Not zerolog, zap, or logrus.
- `encoding/json` for JSON unless profiling shows it's a bottleneck.
- `context.Context` is the first parameter of every function that does I/O. No exceptions.

## HTTP Service Structure

### `func main()` only calls `run()`

The `main` function should be trivial. All real logic goes in a `run` function that takes OS fundamentals as arguments and returns an error. This makes the entire program testable.

```go
func run(ctx context.Context, args []string, getenv func(string) string, stdout, stderr io.Writer) error {
    ctx, cancel := signal.NotifyContext(ctx, os.Interrupt)
    defer cancel()

    // parse config, set up dependencies, start server...
}

func main() {
    ctx := context.Background()
    if err := run(ctx, os.Args, os.Getenv, os.Stdout, os.Stderr); err != nil {
        fmt.Fprintf(os.Stderr, "%s\n", err)
        os.Exit(1)
    }
}
```

Pass `os.Args`, `os.Getenv`, `os.Stdout`, `os.Stderr` as arguments rather than accessing them globally. This lets tests call `run` with different values and run in parallel.

### The `NewServer` constructor

`NewServer` takes all dependencies as explicit arguments and returns an `http.Handler`. It configures its own mux, calls `addRoutes`, and wraps with top-level middleware (CORS, auth, logging).

```go
func NewServer(
    logger *slog.Logger,
    config Config,
    itemStore *item.Store,
) http.Handler {
    mux := http.NewServeMux()
    addRoutes(mux, logger, config, itemStore)
    var handler http.Handler = mux
    handler = withRequestLogging(logger, handler)
    handler = withTraceID(handler)
    return handler
}
```

In tests, pass `nil` for dependencies that won't be used.

### Map the entire API surface in `routes.go`

All routes are listed in a single `addRoutes` function. This is the one place to see the full API surface of the service. Middleware is applied inline so you can see at a glance which routes have which middleware.

```go
func addRoutes(
    mux *http.ServeMux,
    logger *slog.Logger,
    config Config,
    itemStore *item.Store,
) {
    mux.Handle("GET /api/v1/items/{id}", handleGetItem(logger, itemStore))
    mux.Handle("POST /api/v1/items", handleCreateItem(logger, itemStore))
    mux.Handle("GET /healthz", handleHealthz(logger))
    mux.Handle("/", http.NotFoundHandler())
}
```

### Handler maker functions

Handlers are functions that return `http.Handler`, not methods on a server struct. Each handler gets its own closure environment. If a handler needs a dependency, it takes it as an argument.

```go
func handleCreateItem(logger *slog.Logger, store *item.Store) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // ...
    })
}
```

Request and response types can be defined inside the handler function if they're only used there. This keeps the global namespace clean.

```go
func handleCreateItem(logger *slog.Logger, store *item.Store) http.Handler {
    type request struct {
        Name   string `json:"name"`
        SKU    string `json:"sku"`
    }
    type response struct {
        ID string `json:"id"`
    }
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // ...
    })
}
```

### Centralised encode/decode helpers

Handle JSON encoding and decoding in one place. This gives you a single point to change wire format behaviour across all endpoints.

```go
func encode[T any](w http.ResponseWriter, r *http.Request, status int, v T) error {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    if err := json.NewEncoder(w).Encode(v); err != nil {
        return fmt.Errorf("encode json: %w", err)
    }
    return nil
}

func decode[T any](r *http.Request) (T, error) {
    var v T
    if err := json.NewDecoder(r.Body).Decode(&v); err != nil {
        return v, fmt.Errorf("decode json: %w", err)
    }
    return v, nil
}
```

### Validation

Keep validation to things that can be checked locally (required fields, format, range). Database-level checks belong elsewhere.

For struct validation, `go-playground/validator` with struct tags is acceptable — it's a well-established library and avoids hand-rolling validation logic. Wrap validation errors into a project-specific `ValidationErrors` type (see `internal/validation`).

For simple types or domain objects where struct tags are insufficient, add a `Valid` method that returns a map of field problems:

```go
type Validator interface {
    Valid(ctx context.Context) map[string]string
}
```

### Middleware as adapter functions

Middleware takes an `http.Handler` and returns a new one. If middleware has many dependencies, write a constructor that returns the middleware function, keeping `routes.go` clean.

```go
func withRequestLogging(logger *slog.Logger, next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        logger.Info("request", "method", r.Method, "path", r.URL.Path)
        next.ServeHTTP(w, r)
    })
}
```

### Graceful shutdown

Always set up graceful shutdown. Use `signal.NotifyContext` in the `run` function. Use a `WaitGroup` to wait for the server to finish draining. Respect context cancellation at every level.

### Lazy initialisation with `sync.Once`

If a handler needs expensive setup, defer it until the handler is first called. This improves startup time.

```go
func handleTemplate(files ...string) http.Handler {
    var (
        init   sync.Once
        tpl    *template.Template
        tplErr error
    )
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        init.Do(func() {
            tpl, tplErr = template.ParseFiles(files...)
        })
        if tplErr != nil {
            http.Error(w, tplErr.Error(), http.StatusInternalServerError)
            return
        }
        // use tpl
    })
}
```

## Database Access

Use `pgx` directly with SQL strings. No GORM, no ORMs. Use `pgx.NamedArgs` for parameterisation and `pgxpool` for connection pooling.

```go
row := pool.QueryRow(ctx,
    `SELECT id, name, status FROM items WHERE id = @id`,
    pgx.NamedArgs{"id": itemID},
)
```

### Connection pool

The shared package `pkg/database/v1/` provides a thin wrapper around `*pgxpool.Pool`. The wrapper carries metrics registration (Prometheus), health check (`Ping`), and cross-cutting concerns. Do not use a raw pool directly — use the wrapper.

### Transactions

Use the callback-style transaction helper `WithTx(ctx, pool, fn)`. It handles begin, commit, and rollback automatically. Do not manually call `Begin`/`Commit`/`Rollback` unless the callback pattern genuinely cannot express the flow.

### Migrations

Use `pressly/goose/v3` for schema migrations. Goose runs via the `pgx/v5/stdlib` adapter (`database/sql` bridge). Application queries use native `pgxpool`.

Migration SQL files live co-located with the service entry point: `cmd/<service>/migrations/*.sql`. Each service has its own database and embeds its own migrations via `//go:embed`.

### Health checks

DB-backed services extend the existing `/healthz` endpoint to include a `pool.Ping(ctx)` call. No separate readiness probe.

## Error Handling

Errors are values, not strings. Define sentinel errors for known failure modes. Wrap with context using `%w`.

```go
var (
    ErrNotFound  = errors.New("not found")
    ErrDuplicate = errors.New("duplicate")
)

return fmt.Errorf("finding item %s: %w", id, ErrNotFound)
```

## Constructors

Use functional options when a constructor has more than two optional parameters. For simple structs, use a plain constructor. For long dependency lists (like `NewServer`), prefer explicit arguments over a config struct — you get type safety and can't silently skip fields.

## No Package-Level Variables

The only acceptable package-level variables are sentinel errors. No global DB pools, no global loggers. Pass dependencies explicitly through constructors and function arguments.

## Package Structure

Package names describe what's in them, not their architectural role.

```text
internal/
    item/
        item.go          # domain type, validation, sentinel errors
        store.go         # pgx queries
    delivery/
        workflow.go
        consumer.go
pkg/
    database/v1/         # shared pgxpool wrapper, tx helper, goose migration runner
    kafkaenv/            # shared kafka envelope handling
    middleware/          # shared http middleware
cmd/
    service-name/
        main.go          # main() calls run()
        routes.go        # addRoutes() maps the full API surface
        server.go        # NewServer() constructor
        migrations/      # goose SQL migrations (//go:embed)
```

Packages to never create: `service/`, `repository/`, `ports/`, `adapters/`, `driven/`, `driving/`, `utils/`, `helpers/`.

The exception is `internal/domain/` — this is acceptable when it contains the shared aggregate root and domain events that multiple services depend on. The point is to understand the domain (DDD's useful part), not to create ceremonial indirection layers (DDD's harmful part).

### Interfaces

Define interfaces at the consumer site, not alongside the implementation. Do not create an interface unless something needs to mock it or swap implementations.

### No Unnecessary Layers

Do not create a service layer that just delegates to a store. If a handler needs to query the database, call the store directly.

Do not create DTOs that mirror domain structs field-for-field. Unmarshal directly into the domain type and add a `Valid` method. Only create a separate wire type if the format genuinely differs.

## Infrastructure

- Terraform for infrastructure. Schemas for Confluent Cloud managed via data contracts repo.
- Kubernetes deployments via Helm charts in `deploy/`.
- Docker images use multi-stage builds with non-root user.
