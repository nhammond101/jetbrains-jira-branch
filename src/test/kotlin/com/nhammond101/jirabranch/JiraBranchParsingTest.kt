package com.nhammond101.jirabranch

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNull

class JiraBranchParsingTest {

    @Test
    fun `extractIssueKey finds a Jira key in a feature branch`() {
        assertEquals("FSN-123", OpenJiraAction.extractIssueKey("feature/FSN-123-add-login"))
    }

    @Test
    fun `extractIssueKey supports underscores in the project key`() {
        assertEquals("OPS_CORE-42", OpenJiraAction.extractIssueKey("feature/OPS_CORE-42_add-logging"))
    }

    @Test
    fun `extractIssueKey returns the first Jira key when multiple are present`() {
        assertEquals("FSN-123", OpenJiraAction.extractIssueKey("merge/FSN-123-into-PROJ-9"))
    }

    @Test
    fun `extractIssueKey rejects lowercase or mixed-case Jira keys`() {
        assertNull(OpenJiraAction.extractIssueKey("feature/fsn-123-add-login"))
        assertNull(OpenJiraAction.extractIssueKey("feature/Fsn-123-add-login"))
    }

    @Test
    fun `extractIssueKey returns null when the branch has no Jira key`() {
        assertNull(OpenJiraAction.extractIssueKey("feature/no-ticket-here"))
    }
}
