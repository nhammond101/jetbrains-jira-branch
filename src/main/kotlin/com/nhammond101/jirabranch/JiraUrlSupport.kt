package com.nhammond101.jirabranch

import java.net.URI
import java.net.URLEncoder
import java.nio.charset.StandardCharsets

object JiraUrlSupport {
    fun normalizeSiteUrl(value: String): String = value.trim().removeSuffix("/")

    fun isValidSiteUrl(value: String): Boolean {
        val normalized = normalizeSiteUrl(value)
        if (normalized.isBlank()) {
            return false
        }

        return try {
            val uri = URI(normalized)
            (uri.scheme == "http" || uri.scheme == "https") && !uri.host.isNullOrBlank()
        } catch (_: Exception) {
            false
        }
    }

    fun buildIssueUrl(siteUrl: String, issueKey: String): String {
        val encodedIssueKey = URLEncoder.encode(issueKey, StandardCharsets.UTF_8)
        return "${normalizeSiteUrl(siteUrl)}/secure/QuickSearch.jspa?searchString=$encodedIssueKey"
    }
}
