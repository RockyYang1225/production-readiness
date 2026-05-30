import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "install.sh"


class InstallScriptTests(unittest.TestCase):
    def run_install(self, home: Path, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["PRODUCTION_READINESS_REPO_SOURCE"] = str(ROOT)
        return subprocess.run(
            ["bash", str(INSTALL), *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_installs_all_platforms_into_temp_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = self.run_install(home, "all")

            self.assertEqual(result.returncode, 0, result.stderr)
            repo = home / ".production-readiness" / "repo"
            self.assertTrue((repo / "skills/production-readiness/SKILL.md").exists())
            self.assertTrue((home / ".agents/skills/production-readiness").is_symlink())
            self.assertTrue((home / ".claude/skills/production-readiness").is_symlink())
            self.assertTrue((home / "plugins/production-readiness").is_symlink())

            marketplace = json.loads((home / ".agents/plugins/marketplace.json").read_text())
            names = [plugin["name"] for plugin in marketplace["plugins"]]
            self.assertIn("production-readiness", names)

    def test_installs_single_platform_without_other_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = self.run_install(home, "claude")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / ".claude/skills/production-readiness").is_symlink())
            self.assertFalse((home / ".agents/skills/production-readiness").exists())
            self.assertFalse((home / "plugins/production-readiness").exists())

    def test_uninstall_removes_selected_platform_and_marketplace_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertEqual(self.run_install(home, "all").returncode, 0)
            result = self.run_install(home, "--uninstall", "codex")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((home / "plugins/production-readiness").exists())
            self.assertTrue((home / ".claude/skills/production-readiness").exists())
            marketplace = json.loads((home / ".agents/plugins/marketplace.json").read_text())
            names = [plugin["name"] for plugin in marketplace["plugins"]]
            self.assertNotIn("production-readiness", names)


if __name__ == "__main__":
    unittest.main()
