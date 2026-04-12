package com.nhammond101.jirabranch

import kotlin.test.Test
import kotlin.test.assertEquals

class JiraBranchSettingsTest {

    @Test
    fun `loadState normalizes the persisted Jira site URL`() {
        val settings = JiraBranchSettings()

        settings.loadState(
            JiraBranchSettings.State(jiraSiteUrl = "  https://example.atlassian.net/  "),
        )

        assertEquals("https://example.atlassian.net", settings.getJiraSiteUrl())
        assertEquals("https://example.atlassian.net", settings.getState().jiraSiteUrl)
    }

    @Test
    fun `setJiraSiteUrl stores a normalized Jira site URL`() {
        val settings = JiraBranchSettings()

        settings.setJiraSiteUrl(" https://example.atlassian.net/ ")

        assertEquals("https://example.atlassian.net", settings.getJiraSiteUrl())
        assertEquals("https://example.atlassian.net", settings.getState().jiraSiteUrl)
    }
}
