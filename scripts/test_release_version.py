from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts.release_version import determine_release


class ReleaseVersionTest(unittest.TestCase):
    def test_initial_release_uses_plugin_version_when_no_semver_tags_exist(self) -> None:
        repo = self.create_repo()
        self.commit(repo, "feat: initial plugin release")

        plan = determine_release(repo)

        self.assertTrue(plan.should_release)
        self.assertEqual("1.2.0", plan.version)
        self.assertEqual("initial", plan.release_type)
        self.assertEqual("", plan.previous_tag)

    def test_fix_commit_produces_patch_release(self) -> None:
        repo = self.create_repo()
        self.commit(repo, "feat: initial plugin release")
        self.tag(repo, "v1.2.0")
        self.commit(repo, "fix: handle missing branch names")

        plan = determine_release(repo)

        self.assertTrue(plan.should_release)
        self.assertEqual("1.2.1", plan.version)
        self.assertEqual("patch", plan.release_type)
        self.assertEqual("v1.2.0", plan.previous_tag)

    def test_feat_commit_produces_minor_release(self) -> None:
        repo = self.create_repo()
        self.commit(repo, "feat: initial plugin release")
        self.tag(repo, "v1.2.0")
        self.commit(repo, "feat: configurable Jira site URL")

        plan = determine_release(repo)

        self.assertTrue(plan.should_release)
        self.assertEqual("1.3.0", plan.version)
        self.assertEqual("minor", plan.release_type)

    def test_breaking_change_footer_produces_major_release(self) -> None:
        repo = self.create_repo()
        self.commit(repo, "feat: initial plugin release")
        self.tag(repo, "v1.2.0")
        self.commit(
            repo,
            textwrap.dedent(
                """\
                feat: change Jira URL format

                BREAKING CHANGE: Quick search URLs now use a different path.
                """
            ).strip(),
        )

        plan = determine_release(repo)

        self.assertTrue(plan.should_release)
        self.assertEqual("2.0.0", plan.version)
        self.assertEqual("major", plan.release_type)

    def test_breaking_header_produces_major_release(self) -> None:
        repo = self.create_repo()
        self.commit(repo, "feat: initial plugin release")
        self.tag(repo, "v1.2.0")
        self.commit(repo, "feat!: redesign issue parsing")

        plan = determine_release(repo)

        self.assertTrue(plan.should_release)
        self.assertEqual("2.0.0", plan.version)
        self.assertEqual("major", plan.release_type)

    def test_non_release_commits_do_not_create_a_release(self) -> None:
        repo = self.create_repo()
        self.commit(repo, "feat: initial plugin release")
        self.tag(repo, "v1.2.0")
        self.commit(repo, "docs: update README")
        self.commit(repo, "chore: reorganize project metadata")

        plan = determine_release(repo)

        self.assertFalse(plan.should_release)
        self.assertEqual("1.2.0", plan.version)
        self.assertEqual("none", plan.release_type)
        self.assertEqual("v1.2.0", plan.previous_tag)

    def test_head_already_tagged_skips_release(self) -> None:
        repo = self.create_repo()
        self.commit(repo, "feat: initial plugin release")
        self.tag(repo, "v1.2.0")

        plan = determine_release(repo)

        self.assertFalse(plan.should_release)
        self.assertEqual("1.2.0", plan.version)
        self.assertEqual("none", plan.release_type)
        self.assertEqual("v1.2.0", plan.previous_tag)

    def create_repo(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        repo = Path(temp_dir.name)
        self.run_command(repo, "git", "init")
        self.run_command(repo, "git", "config", "user.name", "Test User")
        self.run_command(repo, "git", "config", "user.email", "test@example.com")
        (repo / "gradle.properties").write_text(
            textwrap.dedent(
                """\
                kotlin.stdlib.default.dependency=false
                pluginVersion=1.2.0
                org.gradle.daemon=false
                """
            ),
            encoding="utf-8",
        )
        self.run_command(repo, "git", "add", "gradle.properties")
        self.run_command(repo, "git", "commit", "-m", "chore: add gradle properties")
        return repo

    def commit(self, repo: Path, message: str) -> None:
        current_file = repo / "commits.txt"
        existing = current_file.read_text(encoding="utf-8") if current_file.exists() else ""
        current_file.write_text(existing + message + "\n", encoding="utf-8")
        self.run_command(repo, "git", "add", current_file.name)
        self.run_command(repo, "git", "commit", "-m", message)

    def tag(self, repo: Path, tag_name: str) -> None:
        self.run_command(repo, "git", "tag", tag_name)

    def run_command(self, repo: Path, *args: str) -> None:
        subprocess.run(args, cwd=repo, check=True, capture_output=True, text=True)


if __name__ == "__main__":
    unittest.main()



