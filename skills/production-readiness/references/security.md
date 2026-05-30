# Security Readiness

Review basic production security controls. This is not a penetration test or compliance audit.

## Evidence To Look For

- Secrets are excluded from source control and represented with safe examples.
- Authentication and authorization boundaries are explicit.
- Input validation exists for user-controlled data.
- Sensitive data is not logged or exposed to the browser.
- CORS, cookies, sessions, redirects, and headers have production-safe defaults.
- Dependency vulnerability checks exist or can be run.
- Rate limiting or abuse controls exist for public endpoints.

## Findings To Flag

- `.env`, private keys, tokens, or credentials in the repository.
- Authentication present without authorization checks.
- Client-side code containing private keys or server-only tokens.
- Wide-open CORS on sensitive APIs.
- Missing validation for request bodies, query params, forms, or file uploads.
- Error responses exposing stack traces or internals.

## Ready Evidence

Security is ready for a normal launch only when secrets, auth, validation, sensitive logging, dependency risk, and public attack surfaces have direct evidence.
