package com.nhammond101.jirabranch

import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.Service
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.openapi.components.service

@Service(Service.Level.APP)
@State(name = "JiraBranchSettings", storages = [Storage("jiraBranchOpener.xml")])
class JiraBranchSettings : PersistentStateComponent<JiraBranchSettings.State> {

    data class State(
        var jiraSiteUrl: String = DEFAULT_JIRA_SITE_URL,
    )

    private var state = State()

    override fun getState(): State = state

    override fun loadState(state: State) {
        this.state = state.copy(jiraSiteUrl = normalizeSiteUrl(state.jiraSiteUrl))
    }

    fun getJiraSiteUrl(): String = normalizeSiteUrl(state.jiraSiteUrl)

    fun setJiraSiteUrl(value: String) {
        state = state.copy(jiraSiteUrl = normalizeSiteUrl(value))
    }

    companion object {
        const val DEFAULT_JIRA_SITE_URL = "https://n-able.atlassian.net"

        fun getInstance(): JiraBranchSettings = service()

        fun normalizeSiteUrl(value: String): String = JiraUrlSupport.normalizeSiteUrl(value)

        fun isValidSiteUrl(value: String): Boolean = JiraUrlSupport.isValidSiteUrl(value)
    }
}


