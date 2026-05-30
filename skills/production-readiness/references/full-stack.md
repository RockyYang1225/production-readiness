# Full-Stack Readiness

Review projects where frontend, backend, data, auth, and deployment concerns meet.

## Evidence To Look For

- Frontend/backend contract is explicit and tested.
- Environment configuration is consistent across local, staging, and production.
- Auth flow works across client, server, cookies, sessions, tokens, redirects, and refresh.
- Database migrations and API changes are coordinated.
- Integration tests or end-to-end smoke tests cover critical paths.
- Deployment topology is documented.
- Observability links user-facing failures to backend causes.

## Findings To Flag

- Frontend assumes response shapes not enforced by backend tests or types.
- Local-only URLs, credentials, or CORS settings.
- Auth works locally but lacks production cookie/header settings.
- Database migrations can break older deployed code.
- No end-to-end evidence for critical user flows.

## Ready Evidence

A full-stack project is ready when the deployed frontend, backend, data layer, auth flow, and operations model are verified together.
