# Reliability Readiness

Review how the project behaves when dependencies fail, inputs are unexpected, or traffic increases.

## Evidence To Look For

- Error handling for expected failure modes.
- Timeouts for network calls, database calls, queues, and external APIs.
- Retry behavior with backoff where retries are safe.
- Graceful degradation for optional services.
- Resource limits for uploads, jobs, caches, and memory-heavy operations.
- Startup and shutdown behavior.
- Recovery path for failed jobs or partial operations.

## Findings To Flag

- Unbounded requests, uploads, loops, or background work.
- Retrying non-idempotent operations without safeguards.
- Unhandled promise rejections or broad exception swallowing.
- Single points of failure with no fallback or operator visibility.
- No clear behavior when database, cache, or third-party APIs fail.

## Ready Evidence

Reliability is ready when the most likely failures have intentional behavior, bounded resource use, and observable recovery paths.
