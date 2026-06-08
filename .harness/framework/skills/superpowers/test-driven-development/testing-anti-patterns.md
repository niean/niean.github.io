# Testing Anti-Patterns

Common pitfalls when writing tests. Reference this when adding mocks, test utilities, or complex test setups.

## 1. Testing Mock Behavior Instead of Real Behavior

**The Problem:** Your test passes because the mock returns what you told it to, not because the code works.

```typescript
// BAD: Tests that the mock works, not the code
test('fetches user', async () => {
  const mockFetch = jest.fn().mockResolvedValue({ name: 'Alice' });
  const user = await getUser(mockFetch, 'alice');
  expect(mockFetch).toHaveBeenCalledWith('/users/alice');  // Tests mock was called
  expect(user.name).toBe('Alice');  // Tests mock return value
});

// GOOD: Tests real behavior with minimal isolation
test('fetches user', async () => {
  // Use a real HTTP server (e.g., msw, nock) or in-memory implementation
  server.use(rest.get('/users/alice', (req, res, ctx) => {
    return res(ctx.json({ name: 'Alice' }));
  }));
  const user = await getUser('alice');
  expect(user.name).toBe('Alice');  // Tests actual code path
});
```

**Rule:** If removing the mock would make the test fail for a different reason than "feature missing," you're testing the mock.

## 2. Adding Test-Only Methods to Production Classes

**The Problem:** Production code grows test hooks that weaken encapsulation and create maintenance burden.

```swift
// BAD: Exposing internals for testing
class SessionManager {
    private var sessions: [Session] = []

    // Added just for tests - breaks encapsulation
    func _testGetSessions() -> [Session] { return sessions }
    func _testSetSessions(_ s: [Session]) { sessions = s }
}

// GOOD: Test through public interface
class SessionManager {
    private var sessions: [Session] = []

    func activeSessionCount() -> Int { sessions.filter { $0.isActive }.count }
}

// Test uses public API
func testActiveSessionCount() {
    let manager = SessionManager()
    manager.createSession(name: "test1")
    manager.createSession(name: "test2")
    XCTAssertEqual(manager.activeSessionCount(), 2)
}
```

**Rule:** If you need to expose internals to test, the design needs work. Extract a collaborator, use dependency injection, or test through public behavior.

## 3. Mocking Without Understanding Dependencies

**The Problem:** You mock a dependency because "it's complex" without understanding what it actually does, leading to tests that pass with wrong mocks.

```typescript
// BAD: Blindly mocking a dependency
test('processes order', async () => {
  // What does calculateTax actually return? What format?
  const mockTax = jest.fn().mockReturnValue(10);
  const result = await processOrder(order, { calculateTax: mockTax });
  expect(result.total).toBe(110);
  // If calculateTax actually returns { amount: 10, rate: 0.1 }, this test
  // passes but production code breaks
});

// GOOD: Understand the contract before mocking
test('processes order', async () => {
  // Match the real contract
  const taxCalculator = {
    calculateTax: (amount: number) => ({ amount: amount * 0.1, rate: 0.1 })
  };
  const result = await processOrder(order, taxCalculator);
  expect(result.total).toBe(110);
  expect(result.taxRate).toBe(0.1);
});
```

**Rule:** Before mocking a dependency, read its interface. Your mock must honor the same contract. If you can't describe the contract, you can't safely mock it.

## Summary

| Anti-Pattern | Signal | Fix |
|---|---|---|
| Testing mocks | `expect(mock).toHaveBeenCalled()` is the main assertion | Use real implementations or realistic fakes |
| Test-only methods | Methods prefixed with `_test` or `@VisibleForTesting` | Redesign to test through public interface |
| Blind mocking | `.mockReturnValue()` without checking real return type | Read the dependency's interface first |
