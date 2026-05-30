# Production Readiness

Language: English | [简体中文](README.zh.md)

Production Readiness is an evidence-first review skill and Codex-compatible plugin for checking whether a project is ready for production, launch, release, deployment, or public use.

It helps development agents review demo apps, APIs, web apps, full-stack projects, and general software projects without pretending to be a compliance scanner or automatic launch approval system.

## Supported Review Scopes

- Demo app to production handoff
- API release readiness
- Browser-facing web app launch readiness
- Full-stack project release review
- General project hygiene and maintainability review
- Deployment, observability, reliability, security, data, and testing evidence review

## What This Plugin Provides

- A main skill: `skills/production-readiness/SKILL.md`
- Focused review references in `skills/production-readiness/references/`
- A dependency-free Python inspector: `skills/production-readiness/scripts/inspect_project.py`
- Codex plugin metadata: `.codex-plugin/plugin.json`
- Installation notes for Codex, Claude Code, and other file-based agent tools
- Unit tests and a GitHub Actions workflow for the inspector

## What It Does Not Provide

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

### Codex

Clone the repository:

```bash
git clone https://github.com/RockyYang1225/production-readiness.git
```

Install or point Codex at the local checkout as a plugin. Codex reads:

```text
.codex-plugin/plugin.json
```

The plugin exposes:

```text
skills/production-readiness/SKILL.md
```

### Claude Code

Symlink the skill into Claude Code's skills directory:

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/production-readiness/skills/production-readiness ~/.claude/skills/production-readiness
```

Or copy it:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/production-readiness/skills/production-readiness ~/.claude/skills/
```

### Other Agent Tools

Any tool that supports file-based skills can point at:

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

The inspector detects project type, common ecosystems, framework hints, baseline release signals, missing readiness signals, and evidence paths. It is intentionally lightweight and does not replace manual review.

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

## Repository Readiness Evidence

This repository has been checked with its own production-readiness workflow.

Evidence currently present:

- README: `README.md`
- Installation guide: `INSTALL.md`
- License: `LICENSE`
- Codex plugin manifest: `.codex-plugin/plugin.json`
- Main skill: `skills/production-readiness/SKILL.md`
- Review domains: `skills/production-readiness/references/`
- Inspector script: `skills/production-readiness/scripts/inspect_project.py`
- Unit tests: `tests/test_inspect_project.py`
- CI workflow: `.github/workflows/test.yml`

No runtime secrets or environment variables are required for this repository, so an `.env.example` file is intentionally not included.

## Development Checks

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
