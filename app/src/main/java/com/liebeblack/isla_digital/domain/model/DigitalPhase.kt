package com.liebeblack.isla_digital.domain.model

import kotlinx.serialization.Serializable

/**
 * Fases evolutivas de la Digitalización Humana.
 * Cada fase representa una etapa de madurez digital.
 */
@Serializable
enum class DigitalPhase(
    val displayName: String,
    val ageRange: IntRange,
    val description: String,
    val emoji: String
) {
    SENSORIAL(
        displayName = "Sensorial",
        ageRange = 3..7,
        description = "Exploración táctil, seguridad básica y primeros pasos digitales",
        emoji = "🧸"
    ),
    CREATIVE(
        displayName = "Creativa / Crítica",
        ageRange = 8..14,
        description = "Creación de contenido, ciudadanía digital y lógica de programación",
        emoji = "🎨"
    ),
    PROFESSIONAL(
        displayName = "Profesional / Sistémica",
        ageRange = 15..20,
        description = "IA aplicada, identidad profesional, finanzas y productividad avanzada",
        emoji = "💼"
    );

    companion object {
        fun fromAge(age: Int): DigitalPhase = when {
            age <= 7  -> SENSORIAL
            age <= 14 -> CREATIVE
            else      -> PROFESSIONAL
        }
    }
}
