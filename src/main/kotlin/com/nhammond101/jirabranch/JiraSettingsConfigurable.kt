package com.nhammond101.jirabranch

import com.intellij.openapi.options.Configurable
import com.intellij.openapi.options.ConfigurationException
import com.intellij.ui.components.JBLabel
import com.intellij.ui.components.JBTextField
import com.intellij.util.ui.FormBuilder
import javax.swing.JComponent
import javax.swing.JPanel

class JiraSettingsConfigurable : Configurable {
    private var settingsPanel: JPanel? = null
    private var jiraSiteUrlField: JBTextField? = null

    override fun getDisplayName(): String = "Jira Branch Opener"

    override fun createComponent(): JComponent {
        if (settingsPanel == null) {
            jiraSiteUrlField = JBTextField()

            settingsPanel = FormBuilder.createFormBuilder()
                .addLabeledComponent("Jira site URL:", jiraSiteUrlField!!)
                .addComponent(
                    JBLabel("Example: https://your-company.atlassian.net"),
                    1,
                )
                .addComponentFillVertically(JPanel(), 0)
                .panel
        }

        return settingsPanel!!
    }

    override fun isModified(): Boolean {
        val currentValue = JiraBranchSettings.normalizeSiteUrl(jiraSiteUrlField?.text.orEmpty())
        return currentValue != JiraBranchSettings.getInstance().getJiraSiteUrl()
    }

    @Throws(ConfigurationException::class)
    override fun apply() {
        val currentValue = jiraSiteUrlField?.text.orEmpty()
        if (!JiraBranchSettings.isValidSiteUrl(currentValue)) {
            throw ConfigurationException("Enter a full Jira site URL such as https://your-company.atlassian.net")
        }

        JiraBranchSettings.getInstance().setJiraSiteUrl(currentValue)
        jiraSiteUrlField?.text = JiraBranchSettings.getInstance().getJiraSiteUrl()
    }

    override fun reset() {
        jiraSiteUrlField?.text = JiraBranchSettings.getInstance().getJiraSiteUrl()
    }

    override fun disposeUIResources() {
        settingsPanel = null
        jiraSiteUrlField = null
    }
}

