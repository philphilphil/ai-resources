---
applyTo: '**/*.go,**/*.ts,**/*.tsx,**/*.js,**/*.jsx,**/*.py,**/*.java,**/*.cs,**/*.rs'
description: 'Performance optimization best practices for frontend, backend, and database code.'
---

# Performance Optimization

## General Principles

- **Measure first** — profile before optimizing; use benchmarks and APM tools to find actual bottlenecks
- **Optimize the common case** — focus on hot paths, not rare edge cases
- **Set performance budgets** — define and enforce limits on latency, bundle size, and memory usage
- **Automate** — include performance benchmarks in CI to catch regressions early

## Frontend

- Minimize unnecessary re-renders — use `React.memo`, `useMemo`, `useCallback` appropriately
- Use stable keys in lists; avoid array index keys on dynamic lists
- Lazy-load components and routes with dynamic imports (`React.lazy`, route-level code splitting)
- Use `loading="lazy"` for images and iframes below the fold
- Minify and tree-shake bundles; split vendor vs app code for better caching
- Cache static assets with long-lived `Cache-Control` headers and content-hashed filenames
- Prefer `textContent` over `innerHTML`; batch DOM mutations
- Use CSS transitions/animations (GPU-accelerated) over JS-driven animation loops

## Backend

- Avoid N+1 queries — use eager loading, DataLoader patterns, or batch fetching
- Index columns used in `WHERE`, `JOIN`, and `ORDER BY`; avoid `SELECT *`
- Use connection pooling; never open a new DB connection per request
- Cache expensive, repeated computation (in-memory or Redis); define clear TTL and invalidation strategy
- Paginate, stream, or chunk large payloads — never return unbounded result sets
- Defer non-critical work to background queues
- Avoid blocking I/O on the main thread, goroutine, or event loop
- Use structured logging; avoid logging inside tight hot loops

## Database

- Analyze slow queries with `EXPLAIN` / `EXPLAIN ANALYZE` before adding indexes
- Keep transactions short; use the appropriate isolation level — avoid serializable unless required
- Avoid schema-wide locks; prefer row-level locking
- Archive or partition large tables; purge stale data on a schedule

## Review Checklist

- [ ] Any O(n²) or worse algorithms on large data sets?
- [ ] N+1 queries or unbounded DB reads?
- [ ] Missing indexes on frequently queried columns?
- [ ] Caching applied where appropriate, with correct invalidation?
- [ ] Large payloads paginated or streamed?
- [ ] Memory leaks or unbounded resource growth?
- [ ] Blocking operations in hot paths?
- [ ] Performance-critical paths covered by benchmarks or load tests?
