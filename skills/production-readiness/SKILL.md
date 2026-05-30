---
name: production-readiness
description: Use when reviewing whether a demo app, API, web app, full-stack project, or general software project is ready for production, launch, release, deployment, or public use.
---

# Production Readiness

## Overview

Use this skill to run evidence-first production readiness reviews. A project is not ready because it looks polished, has a README, or is described as a demo; it is ready only when the review finds enough evidence for the intended release scope and risk tolerance.

This skill is a review aid. It is not compliance certification, penetration testing, legal review, or a launch approval substitute for high-risk systems.

## Review Flow

1. Confirm scope: project path, intended deployment target, release audience, project type, and risk tolerance.
2. If local files are available, run:

   ```bash
   python3 skills/production-readiness/scripts/inspect_project.py /path/to/project
   ```

   Use `--json` when a structured handoff is useful.
3. Select reference domains:
   - Always: `references/general.md`, `references/security.md`, `references/testing.md`
   - API: add `references/api.md`
   - Web app: add `references/web-app.md`
   - Full stack: add `references/full-stack.md`, `references/api.md`, `references/web-app.md`, `references/data.md`
   - Deployment or release request: add `references/deployment.md`, `references/observability.md`, `references/reliability.md`
   - Data persistence: add `references/data.md`
4. Gather evidence from source files, configs, docs, tests, logs, screenshots, browser runs, API calls, and command output.
5. Separate verified facts from assumptions. Do not treat framework defaults, README claims, or user intent as proof.
6. Produce the readiness report in the required format.

## Conclusion Rules

- `Ready`: no known launch blockers, key production controls have evidence, and remaining gaps are low risk for the stated release scope.
- `Conditionally Ready`: acceptable for a limited launch, internal deployment, pilot, or demo only under named constraints.
- `Not Ready`: missing critical security, reliability, deployment, data, or verification evidence.

When unsure, choose the more conservative conclusion and state what evidence would change it.

## Required Report Format

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

## Evidence Standards

- Cite files, commands, logs, screenshots, URLs, or code paths for each important finding.
- Say "not verified" when the review did not run a command or inspect a required area.
- Distinguish "test exists" from "test was run and passed."
- Do not claim security, reliability, or deployment readiness without direct evidence.
- Do not silently modify, deploy, archive, delete, or publish the reviewed project.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Marking a demo app ready because it has no users yet | Review the intended audience and data risk anyway |
| Treating README setup as proof | Run or inspect commands and configuration |
| Listing every possible best practice | Focus on blockers, high-risk gaps, and release-relevant improvements |
| Saying "tests pass" without command output | Record the exact command and result |
| Ignoring operations because the app is small | Check deployment, rollback, logs, and health signals at the right scale |

## Minimal Prompt

```text
Use the production-readiness skill to review this project.
Project path: /path/to/project
Scope: full-stack web app
Target deployment: public web deployment
Risk tolerance: low for auth and data
Return blockers, high-risk gaps, evidence, unverified assumptions, and a release checklist.
```
