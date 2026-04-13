# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added
- Added a settings page for configuring the Jira site URL used when opening tickets from the current branch.
- Added GitHub Actions workflows for CI and automated releases.
- Added checked-in `pre-commit` configuration for commit hygiene, Conventional Commit validation, and local pre-push verification.
- Added generation of `jetbrains/updatePlugins.xml` and plugin ZIP publishing for a JetBrains custom plugin repository.

### Changed
- Opening a Jira ticket from the current branch now uses the configured Jira site URL instead of a hardcoded Jira instance.
- Releases from `main` now compute the next semantic version from Conventional Commits and publish plugin artifacts automatically.
- Releases from `main` now also publish custom repository artifacts to the `gh-pages` branch under `jetbrains/`.
- Generated custom repository plugin download URLs now use `raw.githubusercontent.com/<owner>/<repo>/gh-pages/...` and normalize accidental `refs/heads` paths.
- Documented the local hook workflow for Python and Gradle verification before pushes.

## [1.2.0] - 2026-04-12

### Added
- Documented Java 25 toolchain build support in plugin metadata and README.

### Changed
- Bumped plugin version to `1.2.0`.
- Migrated build to `org.jetbrains.intellij.platform` Gradle plugin `2.14.0`.
- Updated Gradle wrapper to `9.1.0`.
- Configured Java and Kotlin toolchains to use Java 25.
- Kept produced bytecode at JVM 17 (`jvmTarget`/`release`) for IntelliJ 2024.1 (`241+`) compatibility.
- Updated distribution references to `jira-branch-opener-1.2.0.zip`.

[1.2.0]: https://github.com/nhammond101/jetbrains-jira-branch/compare/v1.1.0...v1.2.0
