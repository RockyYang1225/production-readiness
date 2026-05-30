# Data Readiness

Review projects that store, process, migrate, or expose persistent data.

## Evidence To Look For

- Clear schema ownership and migration mechanism.
- Validation at boundaries and before persistence.
- Backup and restore plan for production data.
- Retention or deletion behavior for sensitive data.
- Idempotency for writes, webhooks, imports, and retries.
- Protection around destructive actions.
- Privacy-sensitive fields identified and handled carefully.

## Findings To Flag

- Schema changes without migrations.
- Destructive scripts without confirmation or backup guidance.
- No restore test for important data.
- Sensitive fields logged, exported, or exposed unnecessarily.
- Duplicate writes possible during retries.
- Data model assumptions not reflected in constraints.

## Ready Evidence

Data readiness requires proof that important data can be validated, migrated, backed up, restored, protected, and safely modified.
