#!/usr/bin/env python3
"""Inspect a project for production-readiness review signals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SIGNAL_DEFINITIONS = {
    "readme": ("README", ["README.md", "README.rst", "README.txt"]),
    "license": ("License", ["LICENSE", "LICENSE.md", "COPYING"]),
    "env_example": ("Environment example", [".env.example", ".env.sample", "env.example"]),
    "ci_config": ("CI config", [".github/workflows", ".gitlab-ci.yml", "circle.yml", ".circleci/config.yml"]),
    "docker": ("Container/deployment hint", ["Dockerfile", "docker-compose.yml", "compose.yaml", "compose.yml"]),
    "tests": ("Tests", ["tests", "test", "__tests__", "spec", "cypress", "playwright.config.ts", "playwright.config.js"]),
    "health_check": ("Health check hint", ["health", "healthz", "readyz", "livez", "status"]),
}

NODE_FRAMEWORKS = {
    "next": "next",
    "react": "react",
    "vue": "vue",
    "svelte": "svelte",
    "vite": "vite",
    "express": "express",
    "fastify": "fastify",
    "nestjs": "@nestjs/core",
}

PYTHON_FRAMEWORKS = {
    "fastapi": "fastapi",
    "django": "django",
    "flask": "flask",
}


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def list_files(root: Path, limit: int = 4000) -> list[Path]:
    ignored = {".git", "node_modules", ".venv", "venv", "dist", "build", ".next", "target"}
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
            if len(files) >= limit:
                break
    return files


def has_path(root: Path, candidate: str) -> list[str]:
    path = root / candidate
    if path.exists():
        if path.is_dir():
            children = [rel(child, root) for child in sorted(path.iterdir())[:5]]
            return [candidate] + children[:3]
        return [candidate]
    return []


def detect_signals(root: Path, files: list[Path]) -> dict[str, dict[str, Any]]:
    signals: dict[str, dict[str, Any]] = {}
    lower_paths = {rel(path, root).lower(): path for path in files}

    for signal_id, (label, candidates) in SIGNAL_DEFINITIONS.items():
        evidence: list[str] = []
        for candidate in candidates:
            direct = has_path(root, candidate)
            if direct:
                evidence.extend(direct)
                continue
            needle = candidate.lower()
            if signal_id == "health_check":
                evidence.extend(
                    rel(path, root)
                    for lower, path in lower_paths.items()
                    if needle in lower
                )
        signals[signal_id] = {
            "label": label,
            "present": bool(evidence),
            "evidence": sorted(set(evidence))[:10],
        }
    return signals


def detect_node(root: Path) -> tuple[list[str], list[str], list[str]]:
    package_json = root / "package.json"
    if not package_json.exists():
        return [], [], []

    ecosystems = ["node"]
    frameworks: list[str] = []
    evidence = ["package.json"]
    try:
        package = json.loads(package_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ecosystems, frameworks, evidence

    deps: dict[str, Any] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = package.get(key)
        if isinstance(value, dict):
            deps.update(value)

    scripts = package.get("scripts", {})
    script_text = json.dumps(scripts) if isinstance(scripts, dict) else ""
    for name, dep in NODE_FRAMEWORKS.items():
        if dep in deps or name in script_text:
            frameworks.append(name)

    return ecosystems, sorted(set(frameworks)), evidence


def detect_python(root: Path, files: list[Path]) -> tuple[list[str], list[str], list[str]]:
    evidence = []
    for name in ("pyproject.toml", "requirements.txt", "setup.py", "Pipfile"):
        if (root / name).exists():
            evidence.append(name)
    if not evidence:
        return [], [], []

    ecosystems = ["python"]
    text = "\n".join(read_text(root / name).lower() for name in evidence)
    for path in files:
        if path.suffix == ".py" and path.stat().st_size < 200_000:
            text += "\n" + read_text(path).lower()

    frameworks = [name for name, marker in PYTHON_FRAMEWORKS.items() if marker in text]
    return ecosystems, sorted(set(frameworks)), evidence


def detect_other_ecosystems(root: Path) -> tuple[list[str], list[str]]:
    ecosystems = []
    evidence = []
    markers = {
        "go": "go.mod",
        "rust": "Cargo.toml",
        "java": "pom.xml",
        "ruby": "Gemfile",
    }
    for ecosystem, marker in markers.items():
        if (root / marker).exists():
            ecosystems.append(ecosystem)
            evidence.append(marker)
    return ecosystems, evidence


def infer_project_type(root: Path, files: list[Path], frameworks: list[str]) -> str:
    names = {path.name.lower() for path in files}
    rels = {rel(path, root).lower() for path in files}
    dirs = {path.name.lower() for path in root.iterdir() if path.is_dir()}

    has_frontend = bool({"src", "app", "pages", "components", "public"} & dirs) or bool(
        {"react", "vue", "svelte", "vite", "next"} & set(frameworks)
    )
    has_backend = bool({"api", "server", "routes", "controllers"} & dirs) or bool(
        {"express", "fastify", "nestjs", "fastapi", "django", "flask"} & set(frameworks)
    )
    if has_frontend and has_backend:
        return "full-stack"
    if has_backend:
        return "api"
    if has_frontend or "index.html" in names:
        return "web-app"
    if any(path.endswith((".md", ".mdx", ".rst")) for path in rels) and len(files) < 50:
        return "documentation-heavy"
    if {"go.mod", "cargo.toml", "pyproject.toml", "package.json"} & names:
        return "library-or-service"
    return "unknown"


def inspect_project(root: Path) -> dict[str, Any]:
    root = root.resolve()
    files = list_files(root)
    ecosystems: list[str] = []
    frameworks: list[str] = []
    evidence: list[str] = []

    node_ecosystems, node_frameworks, node_evidence = detect_node(root)
    py_ecosystems, py_frameworks, py_evidence = detect_python(root, files)
    other_ecosystems, other_evidence = detect_other_ecosystems(root)

    ecosystems.extend(node_ecosystems + py_ecosystems + other_ecosystems)
    frameworks.extend(node_frameworks + py_frameworks)
    evidence.extend(node_evidence + py_evidence + other_evidence)

    signals = detect_signals(root, files)
    missing = [
        {"id": key, "label": value["label"]}
        for key, value in signals.items()
        if not value["present"] and key in {"readme", "license", "env_example", "ci_config", "tests"}
    ]

    suspicious_files = [
        rel(path, root)
        for path in files
        if path.name in {".env", "id_rsa", "id_dsa"} or path.suffix.lower() in {".pem", ".key"}
    ][:20]

    return {
        "project_root": str(root),
        "project_type": infer_project_type(root, files, frameworks),
        "ecosystems": sorted(set(ecosystems)),
        "frameworks": sorted(set(frameworks)),
        "evidence": sorted(set(evidence)),
        "signals": signals,
        "missing_signals": missing,
        "suspicious_files": suspicious_files,
        "file_count_sampled": len(files),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Project Inspection",
        "",
        f"- Project Root: `{payload['project_root']}`",
        f"- Project Type: `{payload['project_type']}`",
        f"- Ecosystems: {', '.join(payload['ecosystems']) or 'unknown'}",
        f"- Frameworks: {', '.join(payload['frameworks']) or 'unknown'}",
        f"- Files Sampled: {payload['file_count_sampled']}",
        "",
        "## Evidence",
    ]
    if payload["evidence"]:
        lines.extend(f"- `{item}`" for item in payload["evidence"])
    else:
        lines.append("- No ecosystem marker files found.")

    lines.extend(["", "## Release Signals"])
    for signal in payload["signals"].values():
        status = "present" if signal["present"] else "missing"
        lines.append(f"- {signal['label']}: {status}")
        for item in signal["evidence"]:
            lines.append(f"  - `{item}`")

    lines.extend(["", "## Missing Release Signals"])
    if payload["missing_signals"]:
        lines.extend(f"- {item['label']} (`{item['id']}`)" for item in payload["missing_signals"])
    else:
        lines.append("- No required baseline signals missing.")

    if payload["suspicious_files"]:
        lines.extend(["", "## Suspicious Files"])
        lines.extend(f"- `{item}`" for item in payload["suspicious_files"])
        lines.append("")
        lines.append("Use a dedicated secret scanner before release.")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect project readiness signals.")
    parser.add_argument("project", type=Path, help="Project directory to inspect")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")
    args = parser.parse_args()

    if not args.project.exists() or not args.project.is_dir():
        parser.error(f"project directory does not exist: {args.project}")

    payload = inspect_project(args.project)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_markdown(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
