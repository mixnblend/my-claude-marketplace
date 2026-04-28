---
paths:
  - "**/*.go"
---

# Go Code Quality

## Functions Should Be Small and Do One Thing

Decompose long functions into smaller, well-named functions. Each function should do one thing at one level of abstraction. If you find yourself adding a comment to explain what a block of code does, that block should probably be its own function with a name that replaces the comment.

```go
// WRONG — one long function doing many things
func ProcessOrder(ctx context.Context, order Order) error {
    // validate the order
    if order.ID == "" {
        return ErrMissingID
    }
    if len(order.Items) == 0 {
        return ErrNoItems
    }
    for _, item := range order.Items {
        if item.Quantity <= 0 {
            return fmt.Errorf("item %s: %w", item.SKU, ErrInvalidQuantity)
        }
    }

    // calculate totals
    var total int
    for _, item := range order.Items {
        total += item.Price * item.Quantity
    }
    if order.Discount > 0 {
        total -= order.Discount
    }
    if total < 0 {
        total = 0
    }

    // persist
    // ... more code
}

// RIGHT — decomposed into named functions
func ProcessOrder(ctx context.Context, order Order) error {
    if err := order.Validate(); err != nil {
        return fmt.Errorf("validating order: %w", err)
    }

    total := order.CalculateTotal()

    return persistOrder(ctx, order, total)
}
```

## Naming Is Documentation

Names should make the code's intent clear without needing a comment. Invest time in choosing good names — it's the most effective form of documentation.

```go
// WRONG — vague names that require mental mapping
func proc(d []byte) ([]byte, error) { ... }
func handle(w http.ResponseWriter, r *http.Request) { ... }
var m map[string]int

// RIGHT — names that convey intent
func decodeDeliveryInstruction(payload []byte) (DeliveryInstruction, error) { ... }
func handleCreateItem(w http.ResponseWriter, r *http.Request) { ... }
var retryCountByProvider map[string]int
```

For receivers, short names are fine because the type provides context:

```go
func (s *Store) FindByID(ctx context.Context, id uuid.UUID) (Item, error) { ... }
func (i Item) Validate() error { ... }
```

For loop variables in small scopes, short names are acceptable:

```go
for _, item := range items {
    // ...
}
```

## Commenting Philosophy

Comments explain **why**, not **what**. If you need a comment to explain what code does, the code should be rewritten to be self-explanatory — rename the function, extract a variable, decompose into smaller pieces.

```go
// WRONG — comment restates the code
// increment retry count
retryCount++

// WRONG — comment explains what the code does
// loop through items and check if any are expired
for _, item := range items {
    if item.ExpiresAt.Before(time.Now()) {
        expired = append(expired, item)
    }
}

// RIGHT — no comment needed when the code is clear
expiredItems := filterExpired(items)

// RIGHT — comment explains WHY, not what
// The provider API returns 429 with no Retry-After header,
// so we use exponential backoff starting at 500ms.
backoff := 500 * time.Millisecond
```

Acceptable reasons to comment:

- **Why** a non-obvious decision was made
- **Why** a workaround exists (linking to an issue or upstream bug)
- **Why** a particular value was chosen (regulatory requirement, SLA constraint)
- Package-level doc comments describing the package's purpose
- Exported type and function doc comments (godoc) — but only when the name and signature don't already convey the meaning. Omit the comment entirely if it would just restate the function name in sentence form.

Do NOT add comments that categorise or group code (e.g. `// Happy-path cases`, `// Error cases`) or section dividers (e.g. `// --- helpers ---`, `// --- tests ---`). If you need to distinguish groups, extract them into well-named variables or separate test functions instead.

## Function Signatures

Keep function signatures readable. If a function takes more than 3-4 parameters, consider whether some of them should be grouped into a struct or whether the function is doing too much.

```go
// WRONG — too many parameters, hard to read at call sites
func CreateShipment(ctx context.Context, orderID string, items []Item,
    provider string, priority int, scheduledDate time.Time,
    notes string) error { ... }

// RIGHT — group related parameters
type ShipmentRequest struct {
    OrderID       string
    Items         []Item
    Provider      string
    Priority      int
    ScheduledDate time.Time
    Notes         string
}

func CreateShipment(ctx context.Context, req ShipmentRequest) error { ... }
```

## Early Returns

Use early returns to handle errors and edge cases at the top of a function. This keeps the main logic at the lowest indentation level and avoids deeply nested conditionals.

```go
// WRONG — nested conditionals
func ProcessItem(ctx context.Context, id string) error {
    if id != "" {
        item, err := store.Find(ctx, id)
        if err == nil {
            if item.Status == StatusActive {
                // ... main logic buried in nesting
            } else {
                return ErrInactiveItem
            }
        } else {
            return fmt.Errorf("finding item: %w", err)
        }
    } else {
        return ErrMissingID
    }
}

// RIGHT — early returns, main logic at top level
func ProcessItem(ctx context.Context, id string) error {
    if id == "" {
        return ErrMissingID
    }

    item, err := store.Find(ctx, id)
    if err != nil {
        return fmt.Errorf("finding item: %w", err)
    }

    if item.Status != StatusActive {
        return ErrInactiveItem
    }

    // main logic here, unindented
}
```

## Package-Level Organisation

Within a package, organise files by concern, not by type. A package about items should have `item.go` (the type), `store.go` (persistence), and `item_test.go` / `store_test.go` (tests). Not `models.go`, `interfaces.go`, `errors.go` as separate files — keep related things together.

Sentinel errors live in the file that defines the type they relate to, not in a separate `errors.go`.
