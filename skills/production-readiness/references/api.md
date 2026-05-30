# API Readiness

Review HTTP, RPC, webhook, or service APIs before release.

## Evidence To Look For

- Clear API contract through OpenAPI, typed routes, docs, examples, or tests.
- Authentication and authorization on protected endpoints.
- Request validation and response validation where practical.
- Consistent error format and status codes.
- Pagination, filtering, sorting, and limits for list endpoints.
- Idempotency for writes and webhooks where retries are expected.
- Rate limiting or abuse control for public endpoints.
- Integration or contract tests.

## Findings To Flag

- Public endpoints with no auth story.
- Unbounded list endpoints.
- Inconsistent error shapes.
- Request bodies passed directly to persistence.
- No versioning or compatibility plan for external consumers.
- Webhooks without signature verification or replay handling.

## Ready Evidence

An API is ready when its contract, access control, validation, errors, limits, compatibility, and integration tests match the intended consumers.
