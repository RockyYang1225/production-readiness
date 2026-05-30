# Testing Readiness

Review whether tests provide real release evidence.

## Evidence To Look For

- Unit tests for focused business logic.
- Integration tests for boundaries such as database, APIs, queues, and external adapters.
- End-to-end or smoke tests for critical user flows.
- Contract tests for external consumers or providers.
- Regression tests for known failure modes.
- Test data, fixtures, and setup docs.
- Recent command output showing what was actually run.

## Findings To Flag

- Tests exist but were not run.
- Test scripts are missing, stale, or fail locally.
- Critical flows only covered by mocks.
- No negative-path tests for validation, auth, or errors.
- Flaky tests without documented handling.
- Manual QA claims without steps or evidence.

## Ready Evidence

Testing is ready when release-critical behavior has repeatable evidence, and the report clearly states which checks passed, failed, or were not run.
