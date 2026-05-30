# Installation

Production Readiness is distributed as a plain repository. It can be used by Codex, Claude Code, and other agent tools that read file-based skills.

## One-Command Install

macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash
```

Install a single host:

```bash
curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash -s codex
curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash -s claude
curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash -s agents
```

The installer clones or updates the repository at:

```text
~/.production-readiness/repo
```

It then creates symlinks for the selected hosts:

| Host | Installed path |
|---|---|
| Codex | `~/plugins/production-readiness` and `~/.agents/plugins/marketplace.json` |
| Claude Code | `~/.claude/skills/production-readiness` |
| File-based skill tools | `~/.agents/skills/production-readiness` |

## Update

```bash
~/.production-readiness/repo/install.sh --update
```

Update one host:

```bash
~/.production-readiness/repo/install.sh --update codex
~/.production-readiness/repo/install.sh --update claude
~/.production-readiness/repo/install.sh --update agents
```

## Uninstall

```bash
~/.production-readiness/repo/install.sh --uninstall all
```

Uninstall one host:

```bash
~/.production-readiness/repo/install.sh --uninstall codex
~/.production-readiness/repo/install.sh --uninstall claude
~/.production-readiness/repo/install.sh --uninstall agents
```

Uninstall removes symlinks and marketplace entries. It does not delete `~/.production-readiness/repo`.

## Manual Install

Clone the repository:

```bash
git clone https://github.com/RockyYang1225/production-readiness.git
cd production-readiness
```

Codex reads:

```text
.codex-plugin/plugin.json
```

Claude Code can use:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/production-readiness" ~/.claude/skills/production-readiness
```

File-based skill tools can use:

```text
skills/production-readiness/SKILL.md
```

## Verify

Run the inspector against this repository:

```bash
python3 skills/production-readiness/scripts/inspect_project.py .
python3 skills/production-readiness/scripts/inspect_project.py . --json
```

Run tests:

```bash
python3 -m unittest tests/test_inspect_project.py
python3 -m unittest tests/test_install_script.py
```
