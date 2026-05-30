# Production Readiness

[![test](https://github.com/RockyYang1225/production-readiness/actions/workflows/test.yml/badge.svg)](https://github.com/RockyYang1225/production-readiness/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Languages: English | [简体中文](READMEs/README.zh-CN.md)

Evidence-first production readiness reviews for Codex, Claude Code, and other agentic developer tools.

Production Readiness helps development agents decide whether a demo app, API, web app, full-stack project, or general software project is actually ready for launch. It combines a reusable skill, focused review references, and a lightweight project inspector so the review is based on files, commands, and evidence rather than vibes.

[Quick Start](#quick-start) · [Installation](#installation) · [Inspector](#project-inspector) · [Report Format](#review-report-format) · [Verify](#verify-this-repository)

## Contents

- [Why This Exists](#why-this-exists)
- [What It Includes](#what-it-includes)
- [Current Readiness](#current-readiness)
- [Supported Review Scopes](#supported-review-scopes)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Inspector](#project-inspector)
- [Review Report Format](#review-report-format)
- [Verify This Repository](#verify-this-repository)
- [Repository Layout](#repository-layout)
- [Status](#status)
- [License](#license)

## Why This Exists

Demo apps often look polished before they are safe to deploy. Production readiness is less about polish and more about evidence: setup works, tests ran, secrets are handled, deployment is understood, and unverified assumptions are named.

This plugin gives agents a repeatable review path with clear boundaries. It does not certify compliance, perform penetration testing, or make the final release decision for a human owner.

## What It Includes

| Component | Path | Purpose |
|---|---|---|
| Main skill | `skills/production-readiness/SKILL.md` | Guides the agent through evidence-first readiness review |
| Review references | `skills/production-readiness/references/` | Domain checklists for security, reliability, observability, deployment, data, API, web app, full stack, testing, and general readiness |
| Inspector | `skills/production-readiness/scripts/inspect_project.py` | Detects project type, release signals, missing signals, and evidence paths |
| Codex plugin manifest | `.codex-plugin/plugin.json` | Lets Codex recognize this repository as a plugin |
| Installation guide | `INSTALL.md` | Setup notes for Codex, Claude Code, and validation |
| Tests and CI | `tests/test_inspect_project.py`, `.github/workflows/test.yml` | Repeatable verification for the inspector |

## Current Readiness

This repository has been reviewed with its own `production-readiness` skill.

```text
Production Readiness Review

Conclusion: Ready
Scope: Initial public 0.1.0 plugin release
Project Type: documentation-heavy agent skill/plugin repository
Evidence Reviewed: README files, INSTALL.md, LICENSE, Codex manifest, skill files, references, inspector script, tests, CI config, inspector output

Must Fix Before Production:
- None currently known for the initial public plugin release.

High-Risk Gaps:
- None currently known for the initial public plugin release.

Recommended Improvements:
- Add example review reports as the project matures.
- Add release tags once the first version is cut.

Commands / Checks Run:
- python3 -m unittest tests/test_inspect_project.py
- python3 skills/production-readiness/scripts/inspect_project.py .
- python3 skills/production-readiness/scripts/inspect_project.py . --json
- python3 /path/to/plugin-creator/scripts/validate_plugin.py .

Unverified Assumptions:
- Marketplace installation behavior depends on the user's host tool configuration.

Release Checklist:
- README present
- License present
- Plugin manifest present and validated
- Skill and references present
- Inspector script present and tested
- CI workflow present
```

The inspector reports `.env.example` as missing, but this repository has no runtime configuration or secrets. That absence is intentional and not a release blocker.

## Supported Review Scopes

- Demo app to production handoff
- API release readiness
- Browser-facing web app launch readiness
- Full-stack project release review
- General project hygiene and maintainability review
- Deployment, observability, reliability, security, data, and testing evidence review

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

| Host | Setup |
|---|---|
| Codex | Install or point Codex at this checkout. Codex reads `.codex-plugin/plugin.json`. |
| Claude Code | Symlink or copy `skills/production-readiness` into `~/.claude/skills/production-readiness`. |
| Other file-based skill tools | Point the tool at `skills/production-readiness/SKILL.md`. |

Claude Code symlink example:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/production-readiness" ~/.claude/skills/production-readiness
```

Copy instead:

```bash
mkdir -p ~/.claude/skills
cp -R skills/production-readiness ~/.claude/skills/
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

The inspector is intentionally lightweight. It detects project type, common ecosystems, framework hints, baseline release signals, missing readiness signals, suspicious file names, and evidence paths for deeper agent review.

## Review Report Format

Agents using this skill should return:

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
  READMEs/
    README.zh-CN.md
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

MIT. See [LICENSE](LICENSE).
