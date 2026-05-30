# Installation

Production Readiness is distributed as a plain repository. It can be used by Codex, Claude Code, and other agent tools that read file-based skills.

## Codex

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

## Claude Code

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

## Verify The Inspector

Run the inspector against this repository:

```bash
python3 skills/production-readiness/scripts/inspect_project.py .
python3 skills/production-readiness/scripts/inspect_project.py . --json
```

Run tests:

```bash
python3 -m unittest tests/test_inspect_project.py
```
