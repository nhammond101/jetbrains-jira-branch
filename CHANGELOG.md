# Changelog

All notable changes to this project are documented in this file.

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

