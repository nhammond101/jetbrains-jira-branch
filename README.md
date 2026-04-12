# Jira Branch Opener — JetBrains Plugin

A JetBrains IDE plugin that reads the current **Git branch name**, extracts a **Jira issue key** (e.g. `FSN-123`), and opens the matching Jira ticket in your default browser.

Current release: **1.2.0**

## How it works

1. Reads the current branch with `git rev-parse --abbrev-ref HEAD`
2. Scans the branch name for the first match of the pattern `[A-Z][A-Z0-9_]+-\d+` (e.g. `FSN-123`, `PROJ-42`)
3. Opens `https://n-able.atlassian.net/secure/QuickSearch.jspa?searchString=FSN-123` in the default browser

## Usage

| Method | Details |
|--------|---------|
| **Menu** | **Tools → Open Jira Issue from Branch** |
| **Shortcut** | `Ctrl+Shift+J` (Windows/Linux) / `⌃⇧J` (macOS) |

## Build

Builds with a **Java 25** toolchain (Corretto or any JDK 25 distribution).
The plugin bytecode targets **JVM 17** for IntelliJ 2024.1 compatibility.

```bash
JAVA_HOME=/path/to/jdk-25 ./gradlew buildPlugin
```

The built plugin ZIP is located at:
```
build/distributions/jira-branch-opener-1.2.0.zip
```

## Installation

1. Open JetBrains IDE (IntelliJ IDEA, WebStorm, PyCharm, etc.)
2. Go to **Settings → Plugins → ⚙️ → Install Plugin from Disk…**
3. Select `build/distributions/jira-branch-opener-1.2.0.zip`
4. Restart the IDE

## Compatibility

- IntelliJ Platform **2024.1** and later (build `241+`)
- Works in any JetBrains IDE (IntelliJ IDEA, WebStorm, PyCharm, GoLand, Rider, etc.)

## Release Notes

- 1.2.0 migrates to `org.jetbrains.intellij.platform` `2.14.0`
- Build uses Gradle `9.1.0` with Java 25 toolchains
- Distribution artifact: `build/distributions/jira-branch-opener-1.2.0.zip`

See `CHANGELOG.md` for full release history.

