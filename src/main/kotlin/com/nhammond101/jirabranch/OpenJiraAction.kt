package com.nhammond101.jirabranch

import com.intellij.ide.BrowserUtil
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.diagnostic.thisLogger
import com.intellij.openapi.ui.Messages

class OpenJiraAction : AnAction() {

    companion object {
        private val JIRA_ISSUE_PATTERN = Regex("[A-Z][A-Z0-9_]+-\\d+")

        fun extractIssueKey(branchName: String): String? {
            return JIRA_ISSUE_PATTERN.find(branchName)?.value
        }

        fun buildIssueUrl(issueKey: String, jiraSiteUrl: String): String {
            return JiraUrlSupport.buildIssueUrl(jiraSiteUrl, issueKey)
        }
    }

    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return

        // Determine the project base directory
        val basePath = project.basePath
        if (basePath == null) {
            Messages.showWarningDialog(project, "Project has no base directory.", "Jira Branch Opener")
            return
        }

        // Run: git rev-parse --abbrev-ref HEAD
        val branchName = runGit(basePath, "rev-parse", "--abbrev-ref", "HEAD")
        if (branchName == null) {
            Messages.showWarningDialog(
                project,
                "Could not determine the current Git branch.\nMake sure this project is inside a Git repository.",
                "Jira Branch Opener"
            )
            return
        }

        // Extract the first Jira issue key from the branch name (e.g. FSN-123)
        val jiraTicket = extractIssueKey(branchName)
        if (jiraTicket == null) {
            Messages.showInfoMessage(
                project,
                "No Jira issue key found in branch name: \"$branchName\"\n\nExpected a pattern like FSN-123.",
                "Jira Branch Opener"
            )
            return
        }
        val jiraSiteUrl = JiraBranchSettings.getInstance().getJiraSiteUrl()
        val url = buildIssueUrl(jiraTicket, jiraSiteUrl)
        BrowserUtil.browse(url)
    }

    override fun update(e: AnActionEvent) {
        e.presentation.isEnabledAndVisible = e.project != null
    }

    private fun runGit(workDir: String, vararg args: String): String? {
        return try {
            val cmd = listOf("git") + args.toList()
            val process = ProcessBuilder(cmd)
                .directory(java.io.File(workDir))
                .redirectErrorStream(true)
                .start()
            val output = process.inputStream.bufferedReader().readText().trim()
            val exitCode = process.waitFor()
            if (exitCode == 0 && output.isNotEmpty()) output else null
        } catch (ex: Exception) {
            thisLogger().warn("git command failed: ${args.joinToString(" ")}", ex)
            null
        }
    }
}
