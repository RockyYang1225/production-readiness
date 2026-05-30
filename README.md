# Production Readiness

Production Readiness is an agent skill and Codex-compatible plugin for reviewing whether a demo app, API, web app, full-stack project, or general software project is ready for production.

It is designed for evidence-first reviews. The agent should inspect files, configs, docs, tests, logs, screenshots, and command output before calling a project ready.

## What It Checks

- General project hygiene and reproducibility
- Security basics, including secrets, auth, validation, CORS, and sensitive logging
- Reliability, error handling, timeouts, retries, and recovery paths
- Observability, including logs, health checks, metrics, traces, and alertable failures
- Deployment readiness, environment config, release gates, smoke tests, and rollback paths
- Data handling, migrations, backup/restore, validation, privacy, and destructive operations
- API contracts, errors, pagination, idempotency, rate limits, and integration tests
- Web app flows, responsive behavior, accessibility basics, browser errors, and performance
- Full-stack integration across frontend, backend, database, auth, and deployment topology
- Testing evidence, with a clear distinction between tests that exist and tests that were run

## What It Does Not Do

This project does not provide compliance certification, penetration testing, legal review, or a guarantee that a system is safe to launch. It is a structured review aid for development agents and human reviewers.

It does not automatically deploy, modify, or fix the target project.

## Installation

### Codex

Clone this repository from its GitHub page, then install or point Codex at the local checkout.

Codex reads plugin metadata from:

```text
.codex-plugin/plugin.json
```

The plugin exposes its skill from:

```text
skills/production-readiness/SKILL.md
```

### Claude Code

Copy or symlink the skill directory into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/production-readiness/skills/production-readiness ~/.claude/skills/production-readiness
```

Then ask Claude Code for a production-readiness, launch-readiness, or release-readiness review.

### Other Agent Tools

Any agent tool that supports file-based skills can use:

```text
skills/production-readiness/SKILL.md
```

The reference files live in:

```text
skills/production-readiness/references/
```

## Quick Start

Ask your agent:

```text
Use the production-readiness skill to review this project for a production launch.
Scope: full-stack web app.
Project path: /path/to/project.
Target deployment: public web deployment.
Risk tolerance: low for auth, data, and payment flows.
Return blockers, high-risk gaps, evidence, unverified assumptions, and a release checklist.
```

For a narrower API review:

```text
Use the production-readiness skill to review the API layer only.
Focus on auth, validation, error responses, rate limits, idempotency, docs, and integration tests.
```

## Project Inspection Script

This repository includes a lightweight, dependency-free Python script for gathering project signals.

Run it against a project:

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project
```

Output JSON:

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project --json
```

The script is intended to identify useful review signals, not to replace manual inspection. It can detect common project files, likely ecosystems, missing readiness signals, and evidence paths for the agent to review.

## Review Report Format

The skill asks agents to return reports in this shape:

```text
Production Readiness Review

Conclusion: Ready | Conditionally Ready | Not Ready
Scope:
Project Type:
Evidence Reviewed:

Must Fix Before Production:

High-Risk Gaps:

Recommended Improvements:

Domain Findings:

Commands / Checks Run:

Unverified Assumptions:

Release Checklist:
```

Conclusion guidance:

- `Ready`: no known launch blockers, key production controls have evidence, and remaining gaps are low risk.
- `Conditionally Ready`: acceptable for a limited launch, pilot, internal deployment, or demo under named constraints.
- `Not Ready`: missing critical security, reliability, deployment, data, or verification evidence.

## Repository Layout

```text
production-readiness/
  .codex-plugin/
    plugin.json
  INSTALL.md
  LICENSE
  README.md
  skills/
    production-readiness/
      SKILL.md
      references/
      scripts/
        inspect_project.py
  tests/
    test_inspect_project.py
```

## Status

Initial release target: `0.1.0`.

## Development Checks

Run the inspector tests:

```bash
python3 -m unittest tests/test_inspect_project.py
```

Validate the plugin manifest if you have the Codex plugin validator available:

```bash
python3 /Users/rockyyang/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

## License

MIT
