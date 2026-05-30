# Production Readiness Plugin Design

Date: 2026-05-30

## Goal

Build a GitHub-publishable production-readiness review package for agentic developer tools. The first release should work as a neutral repository with a Codex plugin manifest, a Claude Code-compatible skill directory, reusable review references, a lightweight project inspection script, and installation instructions.

The plugin helps agents assess whether a demo app or project is ready for production. It should support API-level reviews, Web app reviews, full-stack project reviews, and general-purpose project reviews.

## Non-Goals

- Do not build a full SaaS scanner or hosted service.
- Do not require network access during a review.
- Do not claim compliance certification such as SOC 2, HIPAA, PCI, or GDPR.
- Do not auto-fix target projects.
- Do not replace manual release approval for high-risk systems.

## Repository Shape

The repository root is:

```text
/Users/rockyyang/Workspace/production-readiness
```

First-release structure:

```text
production-readiness/
  .codex-plugin/
    plugin.json
  skills/
    production-readiness/
      SKILL.md
      references/
        api.md
        data.md
        deployment.md
        full-stack.md
        general.md
        observability.md
        reliability.md
        security.md
        testing.md
        web-app.md
      scripts/
        inspect_project.py
  docs/
    superpowers/
      specs/
        2026-05-30-production-readiness-plugin-design.md
  README.md
  LICENSE
```

## Plugin Identity

Canonical package name:

```text
production-readiness
```

User-facing display name:

```text
Production Readiness
```

Primary trigger language:

- production readiness
- launch readiness
- release readiness
- demo app review
- production上线准备度
- 上线前评审
- 发布前检查

## Core Skill

The main skill lives at:

```text
skills/production-readiness/SKILL.md
```

It should trigger when a user asks an agent to review, inspect, audit, validate, or score whether a project is ready to ship or deploy. It should be explicit that the skill is for agent-assisted review, not for guaranteed compliance or security certification.

The skill workflow:

1. Identify project type and review scope.
2. Run or suggest `inspect_project.py` when local files are available.
3. Select relevant check domains.
4. Gather evidence from source files, docs, configs, tests, logs, screenshots, and command output.
5. Produce a structured readiness report.
6. Mark any unverified claims as assumptions.
7. Recommend the smallest useful next actions.

The skill should default to evidence-first review. It should not mark a project ready based only on README claims, framework defaults, or user intent.

## Check Domains

Each reference file should be concise and focused on one domain. The main skill should load only the domains relevant to the current review.

### General

Applies to any project. Covers purpose clarity, setup reproducibility, dependency hygiene, configuration, licensing, documentation, maintainability, and operational ownership.

### Security

Covers secret handling, authentication, authorization, input validation, dependency vulnerabilities, browser security basics, CORS, rate limiting, secure defaults, and sensitive logging.

### Reliability

Covers error handling, retries, graceful degradation, timeouts, concurrency assumptions, background jobs, resource limits, and recovery paths.

### Observability

Covers logging, metrics, traces, health checks, audit trails, alertable failure modes, and debugging ergonomics.

### Deployment

Covers environment configuration, build scripts, start scripts, deployment docs, runtime requirements, migrations, rollback plans, smoke tests, and release gates.

### Data

Covers schema ownership, migrations, backup/restore, data validation, retention, privacy-sensitive fields, idempotency, and destructive operations.

### API

Covers contract clarity, auth, validation, errors, pagination, idempotency, rate limits, versioning, OpenAPI or equivalent docs, and integration testing.

### Web App

Covers core flows, responsive behavior, accessibility basics, loading/error/empty states, browser errors, form validation, client-side secrets, caching, and performance budget.

### Full Stack

Covers frontend/backend contract, environment parity, database integration, async boundaries, auth flow, deployment topology, integration tests, and end-to-end smoke tests.

### Testing

Covers unit, integration, e2e, smoke, contract, fixture, regression, and manual acceptance evidence. It should distinguish tests that were actually run from tests that merely exist.

## Project Inspection Script

The script lives at:

```text
skills/production-readiness/scripts/inspect_project.py
```

It should be a dependency-free Python 3 script that can run against a project directory:

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project
```

First-release behavior:

- Detect likely project type: API, Web app, full-stack, library, documentation-heavy, or unknown.
- Detect common frameworks and ecosystems from files such as `package.json`, `pyproject.toml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Dockerfile`, `compose.yaml`, `.env.example`, CI configs, and common frontend/backend directories.
- Report evidence paths for detected signals.
- Flag missing release-readiness signals such as missing README, missing tests, missing env example, missing CI config, missing Docker/deployment hints, missing license, and missing health check hints where applicable.
- Output readable Markdown by default.
- Support `--json` for machine-readable output.

The script should not scan secrets deeply in v1. It may flag suspicious filenames and recommend using dedicated secret scanners.

## Readiness Report Format

The skill should produce this report shape:

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

Conclusion rules:

- `Ready`: no known launch-blocking gaps, key production controls have evidence, and remaining items are low risk.
- `Conditionally Ready`: usable for a limited release, pilot, internal deployment, or demo with named constraints.
- `Not Ready`: missing critical security, reliability, deployment, data, or verification evidence.

## Codex Integration

Codex support is provided through:

```text
.codex-plugin/plugin.json
```

The manifest should include:

- name: `production-readiness`
- version: `0.1.0`
- license: `MIT`
- skills path: `./skills/`
- interface metadata with practical starter prompts

No MCP server, app manifest, hooks, or external auth are required for v1.

## Claude Code Integration

Claude Code support should be documented as file-based installation:

- Copy or symlink `skills/production-readiness` into the user's Claude Code skills directory.
- Invoke it by asking for a production-readiness, launch-readiness, or release-readiness review.

The repository should not depend on Claude-specific metadata beyond a standard `SKILL.md` shape.

## README Requirements

`README.md` should include:

- What this project is.
- Supported review scopes.
- What it does and does not guarantee.
- Quick start for Codex.
- Quick start for Claude Code.
- How to run `inspect_project.py`.
- Example review prompt.
- Expected report format.
- Repository layout.
- License.

## Jarvis Workflow Integration

Add a Jarvis workflow:

```text
/Users/rockyyang/Jarvis/90_System/Workflows/Production Readiness Review.md
```

Update:

```text
/Users/rockyyang/Jarvis/90_System/Workflows/Workflows.md
/Users/rockyyang/Jarvis/90_System/Agents/Workflow Registry.md
```

Workflow Chinese name:

```text
生产上线准备度评审
```

Purpose:

Use this workflow before a project, demo app, Web app, API, or full-stack project is considered production-ready or release-ready.

The workflow should clarify:

- Inputs: project path, intended deployment target, acceptable risk, release scope, evidence.
- Outputs: readiness conclusion, blocker list, risk list, verification evidence, next actions.
- Agent boundary: the review agent evaluates readiness but does not silently deploy, archive, delete, rewrite long-term Jarvis knowledge, or send external notifications.
- Human confirmation: required before long-term Jarvis knowledge writes, production deployment, public release, and external communication.

## Quality Bar

Before calling v1 complete:

- Plugin manifest validates with the available plugin validator.
- `inspect_project.py --json` runs against the repository itself.
- `inspect_project.py` Markdown output runs against the repository itself.
- The main skill has valid YAML frontmatter.
- README installation steps are copy-pasteable.
- Jarvis workflow links are updated.
- No unresolved scaffolding markers remain in release files.

## Open Decisions Resolved

- Repository shape: neutral GitHub repo with Codex and Claude Code installation paths.
- License: MIT.
- First release version: `0.1.0`.
- No external services in v1.
- No marketplace entry required for v1 unless explicitly requested later.
