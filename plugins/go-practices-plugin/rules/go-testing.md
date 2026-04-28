---
paths:
  - "**/*_test.go"
---

# Go Testing Conventions

## Assertions with testify

Use `github.com/stretchr/testify/assert` and `github.com/stretchr/testify/require` for assertions. Use `require` when a failure means subsequent checks are meaningless (e.g. a nil pointer would panic). Use `assert` for checks where the test should continue to report multiple failures.

```go
import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestCreateItem(t *testing.T) {
    // Given ... a valid item request
    req := validCreateRequest()

    // When ... the item is created
    created, err := store.Create(ctx, req)

    // Then ... it succeeds and returns the item with an ID
    require.NoError(t, err)
    assert.NotEmpty(t, created.ID)
    assert.Equal(t, "Widget", created.Name)
    assert.Equal(t, StatusCreated, created.Status)
}
```

## Test Organisation

Structure tests using BDD-style comments to make the intent clear. Use `// Given ...`, `// When ...`, `// Then ...` comments (with ellipsis) to separate the phases of each test case. The text after the ellipsis should be descriptive — explain what's being set up, what action is taken, and what the expected outcome is.

```go
func TestTransferFunds(t *testing.T) {
    // Given ... an account with sufficient balance
    account := newAccountWithBalance(t, 1000)
    recipient := newAccountWithBalance(t, 0)

    // When ... a transfer is made
    err := account.TransferTo(ctx, recipient, 500)

    // Then ... both balances are updated
    require.NoError(t, err)
    assert.Equal(t, 500, account.Balance())
    assert.Equal(t, 500, recipient.Balance())
}
```

Use `// And ...` for additional setup steps or additional assertions that are logically distinct from the preceding comment.

```go
    // Given ... a mock processor
    mockProcessor := new(MockStockMessageEventProcessor[StockUpdated])

    // And ... the processor will succeed
    mockProcessor.On("Process", mock.Anything, mock.Anything).Return(nil)
```

## Table-Driven Tests

Use table-driven tests where you're testing the same behaviour with varying inputs and expected outcomes. They reduce duplication and make it easy to add new cases. But don't force everything into a table — if the setup or assertions differ significantly between cases, separate test functions are clearer.

Do not wrap a single test case in a table-driven pattern unless there are clearly more cases that could be added. A standalone test function is simpler and easier to read than a table with one row.

When a table has logical groups of cases, do NOT use inline comments to label the groups. Instead, extract each group into a well-named slice variable and compose them with `append` or `slices.Concat`. The variable name replaces the comment.

```go
func TestParseStatus(t *testing.T) {
    validStatuses := []struct {
        name    string
        input   string
        want    Status
        wantErr error
    }{
        {name: "created", input: "CREATED", want: StatusCreated},
        {name: "shipped", input: "SHIPPED", want: StatusShipped},
    }

    invalidStatuses := []struct {
        name    string
        input   string
        want    Status
        wantErr error
    }{
        {name: "unknown status", input: "BOGUS", wantErr: ErrUnknownStatus},
        {name: "empty string", input: "", wantErr: ErrUnknownStatus},
    }

    tests := slices.Concat(validStatuses, invalidStatuses)

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // When ... the status string is parsed
            got, err := ParseStatus(tt.input)

            // Then ... the result matches expectations
            if tt.wantErr != nil {
                require.ErrorIs(t, err, tt.wantErr)
                return
            }
            require.NoError(t, err)
            assert.Equal(t, tt.want, got)
        })
    }
}
```

## When NOT to Use Table-Driven Tests

If test cases need substantially different setup, different assertions, or the table struct becomes unwieldy with many optional fields, write separate test functions instead. Readability matters more than avoiding repetition.

```go
func TestDelivery_SucceedsOnFirstAttempt(t *testing.T) {
    // Given ... a responsive provider
    provider := newMockProvider(t, withResponse(http.StatusOK))
    svc := delivery.NewService(provider)

    // When ... delivery is attempted
    err := svc.Deliver(ctx, instruction)

    // Then ... it succeeds without retry
    require.NoError(t, err)
    assert.Equal(t, 1, provider.CallCount())
}

func TestDelivery_RetriesOnTransientFailure(t *testing.T) {
    // Given ... a provider that fails once then succeeds
    provider := newMockProvider(t, withResponses(http.StatusServiceUnavailable, http.StatusOK))
    svc := delivery.NewService(provider)

    // When ... delivery is attempted
    err := svc.Deliver(ctx, instruction)

    // Then ... it retries and succeeds
    require.NoError(t, err)
    assert.Equal(t, 2, provider.CallCount())
}
```

## Test Helpers

Use test helper functions to construct valid domain objects. Name them descriptively.

```go
func newAccountWithBalance(t *testing.T, balance int) *Account {
    t.Helper()
    // ...
}

func validItem(t *testing.T) Item {
    t.Helper()
    // ...
}

func itemWithStatus(t *testing.T, status Status) Item {
    t.Helper()
    // ...
}
```

Do not use generic builder patterns (`NewTestItemBuilder().WithName("x").Build()`) when a simple function with clear parameters is sufficient.

## Integration Tests

Separate integration tests from unit tests using a **naming convention**. Integration test files end with `_integration_test.go` and every test function in them is named with an `Integration` prefix.

```go
// item/store_integration_test.go

func TestIntegration_ItemStore_CreateAndRetrieve(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }

    // Given ... a running Postgres container
    ctx := context.Background()
    container := startPostgres(t, ctx)
    pool := connectPool(t, ctx, container)
    store := item.NewStore(pool)

    // When ... an item is created and retrieved
    created, err := store.Create(ctx, validItem(t))
    require.NoError(t, err)

    found, err := store.FindByID(ctx, created.ID)
    require.NoError(t, err)

    // Then ... the retrieved item matches what was created
    assert.Equal(t, created.ID, found.ID)
    assert.Equal(t, created.Name, found.Name)
}
```

Use testcontainers for integration tests that need PostgreSQL, Kafka, or other infrastructure.

### Running tests

Integration tests in this project use `//go:build integration` build tags. They are **not** included in a plain `go test ./...` run.

```bash
# Unit tests only (default — integration tests are excluded by build tag)
go test ./...

# Integration tests (requires build tag)
go test -tags=integration ./...

# Both unit and integration
go test ./... && go test -tags=integration ./...

# Integration tests for a specific package
go test -tags=integration ./pkg/messaging/v1/ -v
```

CI pipelines should run unit tests on every push and integration tests on every PR or merge to main, depending on how long they take.

### Final verification

After implementing any change, always run the full test suite as a final check before committing:

```bash
go vet ./...
go test ./...
go test -tags=integration ./...
```

Do not commit code that breaks existing tests. If integration tests exist for the packages you changed, run them — a plain `go test ./...` is not sufficient.

## Testing HTTP Services via `run`

Prefer end-to-end tests that call the `run` function to start the whole program, then hit the API like a real client. This tests routing, middleware, and handlers together and catches issues that unit testing individual layers misses.

```go
func TestAPI_CreateAndGetItem(t *testing.T) {
    // Given ... a running instance of the service
    ctx, cancel := context.WithCancel(context.Background())
    t.Cleanup(cancel)

    getenv := func(key string) string {
        switch key {
        case "PORT":
            return "0" // let OS pick a free port
        case "DATABASE_URL":
            return testDatabaseURL(t)
        default:
            return ""
        }
    }

    go run(ctx, []string{"myservice"}, getenv, io.Discard, io.Discard)
    waitForReady(t, ctx, "http://localhost:.../healthz")

    // When ... an item is created via the API
    // ... HTTP calls ...

    // Then ... it can be retrieved
    // ... HTTP calls and assertions ...
}
```

This doesn't replace unit tests for complex domain logic, but it reduces the need to separately test boilerplate and wiring.

## Mocking with testify/mock

Use `github.com/stretchr/testify/mock` for unit test mocks. Mocking is a natural benefit of dependency injection — if you accept an interface, you can mock it in tests.

Define mock types in the test file that needs them. If multiple test files in the same package need the same mock, put it in a shared test file (e.g. `mocks_test.go`).

```go
type MockItemStore struct {
    mock.Mock
}

func (m *MockItemStore) FindByID(ctx context.Context, id uuid.UUID) (Item, error) {
    args := m.Called(ctx, id)
    return args.Get(0).(Item), args.Error(1)
}
```

Use `mock.Anything` for arguments you don't care about. Use `mock.AnythingOfType("Type")` when you want type safety without value matching. Use `AssertExpectations(t)` to verify all expected calls were made.

## Testify Usage Guidelines

- Prefer `assert.Equal` over `assert.True(t, a == b)` — the failure message is much more useful.
- Use `require` for preconditions and setup checks. Use `assert` for the actual assertions under test.
- Use `assert.ErrorIs` and `require.ErrorIs` for sentinel error checks, not string matching.
- Use `assert.Contains` for substring checks on error messages only when no sentinel error exists.
- Use `testify/suite` for integration tests that need shared container lifecycle. Do not use suites for unit tests or simple integration tests without shared infrastructure — plain functions are simpler.

## Integration Test Suites

Use `testify/suite` for integration tests that share expensive infrastructure (containers, connections). Suites provide lifecycle hooks that map naturally to container setup/teardown.

### Suite Lifecycle

```go
type ItemRepositorySuite struct {
    suite.Suite
    ctx       context.Context
    container *pgcontainer.PostgresContainer
    pool      *pgxpool.Pool
}

// SetupSuite runs once — start containers, run migrations, take snapshot
func (s *ItemRepositorySuite) SetupSuite() {
    s.ctx = context.Background()
    container, err := pgcontainer.NewPostgresContainer(s.T(), s.ctx,
        pgcontainer.WithMigrations(migrations),
    )
    s.Require().NoError(err)
    s.container = container
    // Seed shared fixtures, then snapshot
    s.Require().NoError(container.Snapshot(s.ctx))
}

// SetupTest runs before each test method — restore DB, reconnect pool
func (s *ItemRepositorySuite) SetupTest() {
    s.Require().NoError(s.container.Restore(s.ctx))
    pool, err := pgxpool.New(s.ctx, s.container.ConnectionString)
    s.Require().NoError(err)
    s.pool = pool
}

// TearDownTest runs after each test method — close pool
func (s *ItemRepositorySuite) TearDownTest() {
    if s.pool != nil {
        s.pool.Close()
    }
}

// TearDownSuite runs once — terminate containers
func (s *ItemRepositorySuite) TearDownSuite() {
    s.Require().NoError(s.container.Terminate(s.ctx))
}

func TestIntegration_ItemRepository(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }
    suite.Run(t, new(ItemRepositorySuite))
}
```

### Postgres: Snapshot/Restore

Use `container.Snapshot(ctx)` after migrations and shared seed data in `SetupSuite`. Use `container.Restore(ctx)` in `SetupTest` to reset state before each test method. Always close and recreate the `pgxpool.Pool` after restore — existing connections become invalid.

### Kafka: Unique Topics Per Test Method

Each test method uses a unique topic name to avoid cross-test data leakage. Topics auto-create on first produce, so no explicit topic creation is needed.

```go
func (s *PublisherSuite) TestPublishSingleEvent() {
    topic := "stock-events-single"  // unique to this test method
    // ...
}

func (s *PublisherSuite) TestPublishMultipleEvents() {
    topic := "stock-events-multiple"  // different topic
    // ...
}
```

### Mixed Postgres+Kafka Suites

For tests needing both Postgres and Kafka, start both containers in `SetupSuite`. Use snapshot/restore for Postgres state isolation and unique topics for Kafka isolation.

### When NOT to Use Suites

- **Unit tests** — plain functions are simpler, no shared state needed.
- **Infrastructure self-tests** (e.g. pool connection tests, migration tests) — these test the infrastructure itself and don't benefit from snapshot/restore.
- **Simple integration tests** with a single test case — the suite overhead isn't justified.
