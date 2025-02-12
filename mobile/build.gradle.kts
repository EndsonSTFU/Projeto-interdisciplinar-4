// build.gradle.kts (ProjetoInterdisciplinar3 - nivel root)

buildscript {
    repositories {
        google() // Repositório do Google
        mavenCentral() // Repositório Central do Maven
    }
    dependencies {
        // Remova a linha abaixo para evitar o conflito:
         classpath("com.android.tools.build:gradle:8.7.2")

        // Versão do Kotlin
        classpath("org.jetbrains.kotlin:kotlin-gradle-plugin:1.7.20")

        // Plugin KSP para processamento de anotações
        classpath("com.google.devtools.ksp:com.google.devtools.ksp.gradle.plugin:2.0.21-1.0.27")
    }
}

plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    id("com.google.devtools.ksp") version "2.0.21-1.0.27" apply false
}
