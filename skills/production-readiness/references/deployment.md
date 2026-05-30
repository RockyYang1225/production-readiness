# Deployment Readiness

Review whether the project can be built, configured, deployed, rolled back, and smoke-tested.

## Evidence To Look For

- Build, start, test, and lint commands.
- Runtime version and package manager requirements.
- Environment variable documentation.
- CI workflow or release gate.
- Container, platform, or infrastructure configuration.
- Database migration plan where applicable.
- Smoke test after deploy.
- Rollback or recovery instructions.

## Findings To Flag

- No production build command.
- Configuration only exists on one developer machine.
- Missing runtime version pinning.
- Migrations run manually with no rollback plan.
- No smoke test or health endpoint for deploy validation.
- Deployment docs conflict with actual scripts.

## Ready Evidence

Deployment is ready when a fresh operator can deploy the intended version to the intended target, verify it, and recover from a bad release.
