package com.liebeblack.isla_digital.domain.model

import kotlinx.serialization.Serializable

/**
 * Configuración del Modo Acompañante (Padres/Tutores).
 * Diseñado para ser informativo y no invasivo.
 */
@Serializable
data class ParentConfig(
    val isEnabled: Boolean = false,
    val parentPin: String = "",
    val dailyTimeLimitMinutes: Int = 60,
    val weeklyReportEnabled: Boolean = true,
    val contentFilterLevel: ContentFilterLevel = ContentFilterLevel.MODERATE,
    val progressNotifications: Boolean = true,
    val activityLog: List<ActivityEntry> = emptyList()
) {
    fun isAccessible(pin: String): Boolean = parentPin == pin
}

@Serializable
enum class ContentFilterLevel(val displayName: String) {
    STRICT("Estricto - Solo contenido educativo básico"),
    MODERATE("Moderado - Contenido educativo con creatividad"),
    OPEN("Abierto - Todo el contenido según la fase")
}

@Serializable
data class ActivityEntry(
    val timestamp: String,
    val action: String,
    val category: String,
    val durationMinutes: Int = 0
)
