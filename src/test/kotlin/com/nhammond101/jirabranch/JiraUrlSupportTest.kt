package com.nhammond101.jirabranch

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

class JiraUrlSupportTest {

    @Test
    fun `normalizeSiteUrl trims whitespace and removes trailing slash`() {
        assertEquals(
            "https://example.atlassian.net",
            JiraUrlSupport.normalizeSiteUrl("  https://example.atlassian.net/  "),
        )
    }

    @Test
    fun `isValidSiteUrl accepts http and https URLs with a host`() {
        assertTrue(JiraUrlSupport.isValidSiteUrl("https://example.atlassian.net"))
        assertTrue(JiraUrlSupport.isValidSiteUrl("http://localhost:8080"))
    }

    @Test
    fun `isValidSiteUrl rejects blank malformed or unsupported URLs`() {
        assertFalse(JiraUrlSupport.isValidSiteUrl(""))
        assertFalse(JiraUrlSupport.isValidSiteUrl("example.atlassian.net"))
        assertFalse(JiraUrlSupport.isValidSiteUrl("ftp://example.atlassian.net"))
        assertFalse(JiraUrlSupport.isValidSiteUrl("https:///missing-host"))
    }

    @Test
    fun `buildIssueUrl normalizes site URL and encodes the issue key`() {
        assertEquals(
            "https://example.atlassian.net/secure/QuickSearch.jspa?searchString=OPS+123%2Ftest",
            JiraUrlSupport.buildIssueUrl("https://example.atlassian.net/", "OPS 123/test"),
        )
    }
}
