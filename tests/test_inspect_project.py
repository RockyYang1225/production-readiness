import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "production-readiness" / "scripts" / "inspect_project.py"


def run_inspector(project: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(project), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class InspectProjectTests(unittest.TestCase):
    def test_detects_full_stack_node_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "package.json").write_text(
                json.dumps(
                    {
                        "scripts": {"test": "vitest", "build": "vite build", "start": "node server.js"},
                        "dependencies": {"next": "15.0.0", "express": "4.0.0"},
                    }
                )
            )
            (project / "app").mkdir()
            (project / "api").mkdir()
            (project / ".github" / "workflows").mkdir(parents=True)
            (project / ".github" / "workflows" / "ci.yml").write_text("name: ci\n")
            (project / ".env.example").write_text("DATABASE_URL=\n")
            (project / "README.md").write_text("# Demo\n")
            (project / "LICENSE").write_text("MIT\n")

            result = run_inspector(project, "--json")

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["project_type"], "full-stack")
            self.assertIn("node", payload["ecosystems"])
            self.assertIn("next", payload["frameworks"])
            self.assertIn("express", payload["frameworks"])
            self.assertTrue(payload["signals"]["ci_config"]["present"])
            self.assertTrue(payload["signals"]["env_example"]["present"])

    def test_flags_missing_release_signals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "package.json").write_text(json.dumps({"scripts": {"start": "vite"}}))
            (project / "src").mkdir()

            result = run_inspector(project, "--json")

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            missing_ids = {item["id"] for item in payload["missing_signals"]}
            self.assertIn("readme", missing_ids)
            self.assertIn("tests", missing_ids)
            self.assertIn("ci_config", missing_ids)
            self.assertIn("env_example", missing_ids)
            self.assertIn("license", missing_ids)

    def test_markdown_output_contains_evidence_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "pyproject.toml").write_text("[project]\nname = 'api-demo'\n")
            (project / "app.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n")
            (project / "README.md").write_text("# API\n")

            result = run_inspector(project)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("# Project Inspection", result.stdout)
            self.assertIn("Project Type:", result.stdout)
            self.assertIn("Evidence", result.stdout)
            self.assertIn("Missing Release Signals", result.stdout)


if __name__ == "__main__":
    unittest.main()
