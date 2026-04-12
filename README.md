# Jira Branch Opener — JetBrains Plugin

A JetBrains IDE plugin that reads the current **Git branch name**, extracts a **Jira issue key** (e.g. `FSN-123`), and opens the matching Jira ticket in your default browser.

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

Requires **Java 17** (Corretto or any JDK 17 distribution).

```bash
JAVA_HOME=/path/to/jdk-17 ./gradlew buildPlugin
```

The built plugin ZIP is located at:
```
build/distributions/jira-branch-opener-1.0.0.zip
```

## Installation

1. Open JetBrains IDE (IntelliJ IDEA, WebStorm, PyCharm, etc.)
2. Go to **Settings → Plugins → ⚙️ → Install Plugin from Disk…**
3. Select `build/distributions/jira-branch-opener-1.0.0.zip`
4. Restart the IDE

## Compatibility

- IntelliJ Platform **2024.1** and later (build `241+`)
- Works in any JetBrains IDE (IntelliJ IDEA, WebStorm, PyCharm, GoLand, Rider, etc.)

