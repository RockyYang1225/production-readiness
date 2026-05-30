# Observability Readiness

Review whether operators can tell what the system is doing and diagnose failures.

## Evidence To Look For

- Structured logs or consistent log fields for important actions.
- Health checks or readiness checks.
- Metrics for traffic, latency, errors, jobs, and resource use.
- Traces or request IDs for multi-service flows.
- Alertable failure modes.
- Audit logs for sensitive or administrative actions.
- Documentation for debugging common incidents.

## Findings To Flag

- No logs around critical user or data flows.
- Logs that expose sensitive data.
- Health checks that only prove the process is alive.
- No way to distinguish user errors, dependency errors, and server bugs.
- No monitoring or alerting plan for public deployment.

## Ready Evidence

Observability is ready when a failure can be detected, triaged, and connected to user impact without reading code from scratch.
