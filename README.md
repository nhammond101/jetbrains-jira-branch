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

- `.github/workflows/build.yml` runs the Python versioning helper tests, Gradle tests, and `buildPlugin` on pushes and pull requests.
- `.github/workflows/release.yml` runs on pushes to `main`, determines the next semantic version from Conventional Commits, builds the plugin, publishes a JetBrains custom repository directory (`jetbrains/updatePlugins.xml` + plugin ZIP) to `gh-pages`, and creates a GitHub release with the generated artifacts.
- The published JetBrains custom repository feed is `https://raw.githubusercontent.com/nhammond101/jetbrains-jira-branch/gh-pages/jetbrains/updatePlugins.xml`.
- The custom repository ZIP download links use the `raw.githubusercontent.com/<owner>/<repo>/gh-pages/jetbrains/...` path.
- The release workflow uses the latest reachable `vX.Y.Z` tag as its baseline. If no semantic version tag exists yet, it creates an initial release using `pluginVersion` from `gradle.properties`.
- Release bumps follow Conventional Commits: `feat` → minor, `fix`/`perf` → patch, and `!` or `BREAKING CHANGE:` → major. Commits such as `docs`, `chore`, and `ci` do not create a release by themselves.

## Local hooks

This repository includes a checked-in `.pre-commit-config.yaml` that protects against common whitespace/YAML mistakes, blocks direct commits to `main`, validates Conventional Commit messages, and mirrors the repo's Python + Gradle verification steps before pushes.

Install the hooks after bootstrapping local tooling:

```bash
brew bundle
pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

Run the hooks on demand:

```bash
pre-commit run --all-files
cz check -m "feat: verify local hook setup"
make python-test-release-version
make gradle-verify
```

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

### Install from the published plugin repository

1. Open your JetBrains IDE (IntelliJ IDEA, WebStorm, PyCharm, etc.)
2. Go to **Settings / Preferences → Plugins**
3. Click the gear icon and choose **Manage Plugin Repositories…**
4. Add this custom repository URL:

   ```text
   https://raw.githubusercontent.com/nhammond101/jetbrains-jira-branch/gh-pages/jetbrains/updatePlugins.xml
   ```

5. Close the repository dialog, search for **Jira Branch Opener**, and install it from the Marketplace / custom repositories list
6. Restart the IDE when prompted

> Do not use the `.../refs/heads/gh-pages/...` form of the URL. JetBrains should be pointed at the `.../gh-pages/jetbrains/updatePlugins.xml` feed above.

### Install from a local ZIP (fallback)

1. Build the plugin or download a release ZIP
2. Go to **Settings / Preferences → Plugins → ⚙️ → Install Plugin from Disk…**
3. Select `build/distributions/jira-branch-opener-<version>.zip`
4. Restart the IDE

## Compatibility

- IntelliJ Platform **2024.1** and later (build `241+`)
- Works in any JetBrains IDE (IntelliJ IDEA, WebStorm, PyCharm, GoLand, Rider, etc.)

## Release Notes

See GitHub Releases and `CHANGELOG.md` for published versions and notable changes.
