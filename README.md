# Production Readiness

[![test](https://github.com/RockyYang1225/production-readiness/actions/workflows/test.yml/badge.svg)](https://github.com/RockyYang1225/production-readiness/actions/workflows/test.yml)

Language: English | [简体中文](README.zh.md)

Production Readiness is an evidence-first review skill and Codex-compatible plugin for checking whether a project is ready for production, launch, release, deployment, or public use.

It gives development agents a repeatable way to review demo apps, APIs, web apps, full-stack projects, and general software projects without pretending to be a compliance scanner or automatic launch approval system.

## At A Glance

| Part | Path | Purpose |
|---|---|---|
| Main skill | `skills/production-readiness/SKILL.md` | Guides the agent through the review |
| Review domains | `skills/production-readiness/references/` | Focused checklists for security, deployment, API, web, data, testing, and more |
| Inspector | `skills/production-readiness/scripts/inspect_project.py` | Detects project type and baseline release signals |
| Codex plugin | `.codex-plugin/plugin.json` | Lets Codex recognize this repository as a plugin |
| Install guide | `INSTALL.md` | Copy-pasteable setup notes |

## When To Use It

Use this plugin when you want an agent to answer questions like:

- Is this demo app actually ready for production?
- What blocks this API from being released?
- What are the highest-risk gaps before deploying this web app?
- Which checks were verified, and which are still assumptions?
- Can this project launch only under limited conditions?

## What It Reviews

- General project hygiene and reproducibility
- Security basics: secrets, auth, validation, CORS, dependency risk, sensitive logging
- Reliability: errors, timeouts, retries, resource limits, recovery paths
- Observability: logs, health checks, metrics, traces, alertable failures
- Deployment: build/start/test commands, CI, runtime requirements, smoke tests, rollback
- Data: migrations, backups, validation, retention, destructive operations
- API readiness: contracts, errors, pagination, idempotency, rate limits, integration tests
- Web app readiness: core flows, responsive behavior, accessibility basics, browser errors
- Testing evidence, with a clear split between "tests exist" and "tests were run"

## Boundaries

This project does not provide compliance certification, penetration testing, legal review, or a guarantee that a system is safe to launch.

It does not automatically deploy, modify, or fix the target project. The review should separate verified evidence from assumptions and leave release decisions to the human owner.

## Quick Start

Ask your agent:

```text
Use the production-readiness skill to review this project.
Project path: /path/to/project
Scope: full-stack web app
Target deployment: public web deployment
Risk tolerance: low for auth and data
Return blockers, high-risk gaps, evidence, unverified assumptions, and a release checklist.
```

For an API-only review:

```text
Use the production-readiness skill to review the API layer only.
Focus on auth, validation, error responses, pagination, rate limits, idempotency, docs, and integration tests.
```

## Installation

Clone the repository:

```bash
git clone https://github.com/RockyYang1225/production-readiness.git
cd production-readiness
```

### Codex

Install or point Codex at the local checkout. Codex reads:

```text
.codex-plugin/plugin.json
```

### Claude Code

Symlink the skill:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/production-readiness" ~/.claude/skills/production-readiness
```

Or copy it:

```bash
mkdir -p ~/.claude/skills
cp -R skills/production-readiness ~/.claude/skills/
```

### Other Agent Tools

Point any file-based skill system at:

```text
skills/production-readiness/SKILL.md
```

## Project Inspector

Run the inspector against a project:

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project
```

Output JSON:

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project --json
```

The inspector is intentionally lightweight. It detects project type, common ecosystems, framework hints, baseline release signals, missing readiness signals, and evidence paths for deeper agent review.

## Review Output

The skill asks agents to return this report shape:

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

## Verify This Repository

Run tests:

```bash
python3 -m unittest tests/test_inspect_project.py
```

Run the inspector against this repository:

```bash
python3 skills/production-readiness/scripts/inspect_project.py .
python3 skills/production-readiness/scripts/inspect_project.py . --json
```

Validate the Codex plugin manifest when the validator is available:

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
```

Current repository evidence:

- README: `README.md`, `README.zh.md`
- Installation guide: `INSTALL.md`
- License: `LICENSE`
- Codex plugin manifest: `.codex-plugin/plugin.json`
- Main skill: `skills/production-readiness/SKILL.md`
- Review domains: `skills/production-readiness/references/`
- Inspector script: `skills/production-readiness/scripts/inspect_project.py`
- Unit tests: `tests/test_inspect_project.py`
- CI workflow: `.github/workflows/test.yml`

No runtime secrets or environment variables are required for this repository, so `.env.example` is intentionally not included.

## Repository Layout

```text
production-readiness/
  .codex-plugin/
    plugin.json
  .github/
    workflows/
      test.yml
  INSTALL.md
  LICENSE
  README.md
  README.zh.md
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

## License

MIT
