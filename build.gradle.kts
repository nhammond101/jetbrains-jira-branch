plugins {
    id("java")
    id("org.jetbrains.kotlin.jvm") version "1.9.24"
    id("org.jetbrains.intellij") version "1.17.4"
}

group = "com.nhammond101"
version = "1.0.0"

repositories {
    mavenCentral()
}

kotlin {
    jvmToolchain(17)
}

intellij {
    version.set("2024.1.7")
    type.set("IC") // IntelliJ IDEA Community Edition
    plugins.set(listOf())
}

tasks {
    buildSearchableOptions {
        enabled = false
    }

    patchPluginXml {
        sinceBuild.set("241")
        untilBuild.set("")   // empty = no upper bound, compatible with all future IDE versions
    }
}

