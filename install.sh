#!/usr/bin/env bash
set -euo pipefail

PLUGIN_NAME="production-readiness"
REPO_URL="${PRODUCTION_READINESS_REPO_SOURCE:-https://github.com/RockyYang1225/production-readiness.git}"
INSTALL_ROOT="${PRODUCTION_READINESS_HOME:-$HOME/.production-readiness}"
REPO_DIR="${PRODUCTION_READINESS_REPO_DIR:-$INSTALL_ROOT/repo}"
AGENTS_SKILLS_DIR="${PRODUCTION_READINESS_AGENTS_SKILLS_DIR:-$HOME/.agents/skills}"
CLAUDE_SKILLS_DIR="${PRODUCTION_READINESS_CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
CODEX_PLUGINS_DIR="${PRODUCTION_READINESS_CODEX_PLUGINS_DIR:-$HOME/plugins}"
MARKETPLACE_PATH="${PRODUCTION_READINESS_MARKETPLACE_PATH:-$HOME/.agents/plugins/marketplace.json}"

usage() {
  cat <<'EOF'
Production Readiness installer

Usage:
  install.sh [all|codex|claude|agents]
  install.sh --update [all|codex|claude|agents]
  install.sh --uninstall [all|codex|claude|agents]

Examples:
  curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash
  curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash -s codex
  ./install.sh --update
  ./install.sh --uninstall claude
EOF
}

log() {
  printf '%s\n' "production-readiness: $*"
}

die() {
  printf '%s\n' "production-readiness: $*" >&2
  exit 1
}

ensure_repo() {
  mkdir -p "$INSTALL_ROOT"
  if [ -d "$REPO_DIR/.git" ]; then
    log "updating $REPO_DIR"
    git -C "$REPO_DIR" pull --ff-only >/dev/null
  elif [ -e "$REPO_DIR" ]; then
    die "$REPO_DIR exists but is not a git repository"
  else
    log "cloning $REPO_URL to $REPO_DIR"
    git clone "$REPO_URL" "$REPO_DIR" >/dev/null
  fi
}

ensure_link() {
  local source=$1
  local target=$2
  mkdir -p "$(dirname "$target")"
  if [ -L "$target" ]; then
    rm "$target"
  elif [ -e "$target" ]; then
    die "$target already exists and is not a symlink"
  fi
  ln -s "$source" "$target"
}

remove_link() {
  local target=$1
  if [ -L "$target" ]; then
    rm "$target"
  elif [ -e "$target" ]; then
    die "$target exists and is not a symlink; remove it manually if intended"
  fi
}

update_marketplace() {
  mkdir -p "$(dirname "$MARKETPLACE_PATH")"
  MARKETPLACE_PATH="$MARKETPLACE_PATH" python3 - <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["MARKETPLACE_PATH"])
if path.exists():
    data = json.loads(path.read_text())
else:
    data = {"name": "personal", "interface": {"displayName": "Personal"}, "plugins": []}

data.setdefault("name", "personal")
data.setdefault("interface", {}).setdefault("displayName", "Personal")
plugins = [p for p in data.get("plugins", []) if p.get("name") != "production-readiness"]
plugins.append({
    "name": "production-readiness",
    "source": {"source": "local", "path": "./plugins/production-readiness"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Development",
})
data["plugins"] = plugins
path.write_text(json.dumps(data, indent=2) + "\n")
PY
}

remove_marketplace_entry() {
  [ -f "$MARKETPLACE_PATH" ] || return 0
  MARKETPLACE_PATH="$MARKETPLACE_PATH" python3 - <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["MARKETPLACE_PATH"])
data = json.loads(path.read_text())
data["plugins"] = [p for p in data.get("plugins", []) if p.get("name") != "production-readiness"]
path.write_text(json.dumps(data, indent=2) + "\n")
PY
}

install_agents() {
  ensure_link "$REPO_DIR/skills/$PLUGIN_NAME" "$AGENTS_SKILLS_DIR/$PLUGIN_NAME"
  log "installed agents skill: $AGENTS_SKILLS_DIR/$PLUGIN_NAME"
}

install_claude() {
  ensure_link "$REPO_DIR/skills/$PLUGIN_NAME" "$CLAUDE_SKILLS_DIR/$PLUGIN_NAME"
  log "installed Claude Code skill: $CLAUDE_SKILLS_DIR/$PLUGIN_NAME"
}

install_codex() {
  ensure_link "$REPO_DIR" "$CODEX_PLUGINS_DIR/$PLUGIN_NAME"
  update_marketplace
  log "installed Codex plugin: $CODEX_PLUGINS_DIR/$PLUGIN_NAME"
  log "updated marketplace: $MARKETPLACE_PATH"
}

uninstall_agents() {
  remove_link "$AGENTS_SKILLS_DIR/$PLUGIN_NAME"
  log "removed agents skill: $AGENTS_SKILLS_DIR/$PLUGIN_NAME"
}

uninstall_claude() {
  remove_link "$CLAUDE_SKILLS_DIR/$PLUGIN_NAME"
  log "removed Claude Code skill: $CLAUDE_SKILLS_DIR/$PLUGIN_NAME"
}

uninstall_codex() {
  remove_link "$CODEX_PLUGINS_DIR/$PLUGIN_NAME"
  remove_marketplace_entry
  log "removed Codex plugin: $CODEX_PLUGINS_DIR/$PLUGIN_NAME"
  log "updated marketplace: $MARKETPLACE_PATH"
}

run_for_platform() {
  local action=$1
  local platform=$2
  case "$platform" in
    all)
      run_for_platform "$action" codex
      run_for_platform "$action" claude
      run_for_platform "$action" agents
      ;;
    codex|claude|agents)
      "${action}_${platform}"
      ;;
    *)
      usage
      die "unknown platform: $platform"
      ;;
  esac
}

main() {
  local action="install"
  local platform="all"

  case "${1:-}" in
    -h|--help)
      usage
      exit 0
      ;;
    --update)
      action="install"
      platform="${2:-all}"
      ;;
    --uninstall)
      action="uninstall"
      platform="${2:-all}"
      ;;
    "")
      ;;
    *)
      platform="$1"
      ;;
  esac

  if [ "$action" = "install" ]; then
    ensure_repo
  fi

  run_for_platform "$action" "$platform"
  log "done"
}

main "$@"
