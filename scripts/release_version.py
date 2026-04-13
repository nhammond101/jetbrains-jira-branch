from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SEMVER_TAG_PATTERN = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
CONVENTIONAL_HEADER_PATTERN = re.compile(r"^(?P<type>[a-z]+)(?:\([^)]+\))?(?P<breaking>!)?:\s+")
BREAKING_CHANGE_PATTERN = re.compile(r"^BREAKING[ -]CHANGE:\s+", re.MULTILINE)


@dataclass(frozen=True, order=True)
class SemVer:
    major: int
    minor: int
    patch: int

    def bump(self, release_type: str) -> "SemVer":
        if release_type == "major":
            return SemVer(self.major + 1, 0, 0)
        if release_type == "minor":
            return SemVer(self.major, self.minor + 1, 0)
        if release_type == "patch":
            return SemVer(self.major, self.minor, self.patch + 1)
        raise ValueError(f"Unsupported release type: {release_type}")

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class ReleasePlan:
    should_release: bool
    version: str
    release_type: str
    previous_tag: str
    commits_considered: int
    reason: str

    def to_outputs(self) -> dict[str, str]:
        return {
            "should_release": str(self.should_release).lower(),
            "version": self.version,
            "release_type": self.release_type,
            "previous_tag": self.previous_tag,
            "commits_considered": str(self.commits_considered),
            "reason": self.reason,
        }


def run_git(repo_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def parse_semver_tag(tag: str) -> SemVer | None:
    match = SEMVER_TAG_PATTERN.fullmatch(tag.strip())
    if match is None:
        return None
    return SemVer(*(int(part) for part in match.groups()))


def read_default_version(repo_root: Path) -> str:
    gradle_properties = repo_root / "gradle.properties"
    for raw_line in gradle_properties.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("pluginVersion="):
            return line.split("=", 1)[1].strip()
    raise ValueError("pluginVersion was not found in gradle.properties")


def get_reachable_semver_tags(repo_root: Path) -> list[tuple[SemVer, str]]:
    output = run_git(repo_root, "tag", "--merged", "HEAD")
    tags = []
    for raw_tag in output.splitlines():
        tag = raw_tag.strip()
        if not tag:
            continue
        version = parse_semver_tag(tag)
        if version is not None:
            tags.append((version, tag))
    return sorted(tags)


def get_semver_tags_pointing_at_head(repo_root: Path) -> list[str]:
    output = run_git(repo_root, "tag", "--points-at", "HEAD")
    return [tag for tag in output.splitlines() if parse_semver_tag(tag) is not None]


def get_commit_messages(repo_root: Path, revision_range: str) -> list[str]:
    output = run_git(repo_root, "log", "--format=%B%x00", revision_range)
    return [message.strip() for message in output.split("\x00") if message.strip()]


def classify_commit(message: str) -> str | None:
    if BREAKING_CHANGE_PATTERN.search(message):
        return "major"

    header = next((line.strip() for line in message.splitlines() if line.strip()), "")
    match = CONVENTIONAL_HEADER_PATTERN.match(header)
    if match is None:
        return None
    if match.group("breaking"):
        return "major"
    if match.group("type") == "feat":
        return "minor"
    if match.group("type") in {"fix", "perf"}:
        return "patch"
    return None


def highest_release_type(release_types: Iterable[str | None]) -> str | None:
    precedence = {"major": 3, "minor": 2, "patch": 1, None: 0}
    highest = None
    for release_type in release_types:
        if precedence[release_type] > precedence[highest]:
            highest = release_type
    return highest


def determine_release(repo_root: Path) -> ReleasePlan:
    default_version = read_default_version(repo_root)
    tags_at_head = get_semver_tags_pointing_at_head(repo_root)
    if tags_at_head:
        head_tag = max(tags_at_head, key=lambda tag: parse_semver_tag(tag) or SemVer(0, 0, 0))
        return ReleasePlan(
            should_release=False,
            version=str(parse_semver_tag(head_tag)),
            release_type="none",
            previous_tag=head_tag,
            commits_considered=0,
            reason="HEAD is already tagged with a semantic version.",
        )

    reachable_tags = get_reachable_semver_tags(repo_root)
    latest_version, latest_tag = reachable_tags[-1] if reachable_tags else (None, "")

    if latest_version is None:
        return ReleasePlan(
            should_release=True,
            version=default_version,
            release_type="initial",
            previous_tag="",
            commits_considered=0,
            reason="No semantic version tags were found; using pluginVersion as the initial release.",
        )

    commits = get_commit_messages(repo_root, f"{latest_tag}..HEAD")
    if not commits:
        return ReleasePlan(
            should_release=False,
            version=str(latest_version),
            release_type="none",
            previous_tag=latest_tag,
            commits_considered=0,
            reason="No commits were found since the latest semantic version tag.",
        )

    release_type = highest_release_type(classify_commit(commit) for commit in commits)
    if release_type is None:
        return ReleasePlan(
            should_release=False,
            version=str(latest_version),
            release_type="none",
            previous_tag=latest_tag,
            commits_considered=len(commits),
            reason=f"No release-triggering Conventional Commits were found since {latest_tag}.",
        )

    next_version = latest_version.bump(release_type)
    return ReleasePlan(
        should_release=True,
        version=str(next_version),
        release_type=release_type,
        previous_tag=latest_tag,
        commits_considered=len(commits),
        reason=f"Computed a {release_type} release from {len(commits)} commit(s) since {latest_tag}.",
    )


def write_github_outputs(github_output: Path, plan: ReleasePlan) -> None:
    with github_output.open("a", encoding="utf-8") as handle:
        for key, value in plan.to_outputs().items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Determine the next release version from conventional commits.")
    parser.add_argument("--repo-root", default=".", help="Path to the git repository root.")
    parser.add_argument(
        "--github-output",
        help="Optional path to the GitHub Actions output file to populate with computed values.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    plan = determine_release(repo_root)

    if args.github_output:
        write_github_outputs(Path(args.github_output), plan)
    else:
        print(json.dumps(plan.to_outputs(), indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
