# Jira Branch Opener — JetBrains Plugin

A JetBrains IDE plugin that reads the current **Git branch name**, extracts a **Jira issue key** (e.g. `FSN-123`), and opens the matching Jira ticket in your default browser.

Releases are published from `main` and versioned automatically from Conventional Commits.

## How it works

1. Reads the current branch with `git rev-parse --abbrev-ref HEAD`
2. Scans the branch name for the first match of the pattern `[A-Z][A-Z0-9_]+-\d+` (e.g. `FSN-123`, `PROJ-42`)
3. Opens `<configured-jira-site>/secure/QuickSearch.jspa?searchString=FSN-123` in the default browser

The Jira site URL is configurable from **Settings → Tools → Jira Branch Opener**.
If you do not change it, the plugin defaults to `https://n-able.atlassian.net`.

## Automation

- `.github/workflows/ci.yml` runs the Python versioning helper tests, Gradle tests, and `buildPlugin` on pushes and pull requests.
- `.github/workflows/release.yml` runs on pushes to `main`, determines the next semantic version from Conventional Commits, builds the plugin, and creates a GitHub release with the generated artifacts.
- The release workflow uses the latest reachable `vX.Y.Z` tag as its baseline. If no semantic version tag exists yet, it creates an initial release using `pluginVersion` from `gradle.properties`.
- Release bumps follow Conventional Commits: `feat` → minor, `fix`/`perf` → patch, and `!` or `BREAKING CHANGE:` → major. Commits such as `docs`, `chore`, and `ci` do not create a release by themselves.

## Usage

| Method | Details |
|--------|---------|
| **Menu** | **Tools → Open Jira Issue from Branch** |
| **Shortcut** | `Ctrl+Shift+J` (Windows/Linux) / `⌃⇧J` (macOS) |

### Jira site configuration

1. Open **Settings** / **Preferences**
2. Go to **Tools → Jira Branch Opener**
3. Enter your Jira site URL, for example `https://your-company.atlassian.net`
4. Apply the change and use **Open Jira Issue from Branch** as usual

## Build

Builds with a **Java 25** toolchain (Corretto or any JDK 25 distribution).
The plugin bytecode targets **JVM 17** for IntelliJ 2024.1 compatibility.

```bash
JAVA_HOME=/path/to/jdk-25 ./gradlew buildPlugin
```

The built plugin ZIP is located at:
```
build/distributions/jira-branch-opener-<version>.zip
```

## Installation

1. Open JetBrains IDE (IntelliJ IDEA, WebStorm, PyCharm, etc.)
2. Go to **Settings → Plugins → ⚙️ → Install Plugin from Disk…**
3. Select `build/distributions/jira-branch-opener-<version>.zip`
4. Restart the IDE

## Compatibility

- IntelliJ Platform **2024.1** and later (build `241+`)
- Works in any JetBrains IDE (IntelliJ IDEA, WebStorm, PyCharm, GoLand, Rider, etc.)

## Release Notes

See GitHub Releases and `CHANGELOG.md` for published versions and notable changes.

