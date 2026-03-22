package com.liebeblack.isla_digital.domain.model

import kotlinx.serialization.Serializable

/**
 * Certificaciones internas que validan competencias adquiridas.
 * Cada certificación se desbloquea al completar un conjunto de habilidades.
 */
@Serializable
enum class CertificationType(
    val displayName: String,
    val description: String,
    val requiredPhase: DigitalPhase,
    val requiredSkillIds: List<String>,
    val badgeColor: Long, // Color en formato ARGB
    val tier: Int
) {
    SAFE_USER(
        displayName = "Usuario Seguro",
        description = "Has demostrado conocer las bases de la seguridad en línea y la protección personal",
        requiredPhase = DigitalPhase.SENSORIAL,
        requiredSkillIds = listOf("sec_01", "sec_02", "sec_03"),
        badgeColor = 0xFF00C853, // Verde
        tier = 1
    ),
    DEVICE_NAVIGATOR(
        displayName = "Navegador del Dispositivo",
        description = "Dominas las herramientas básicas y la interacción con tu dispositivo",
        requiredPhase = DigitalPhase.SENSORIAL,
        requiredSkillIds = listOf("dev_01", "dev_02", "dev_03", "web_01", "web_02"),
        badgeColor = 0xFF1E90FF, // Azul
        tier = 1
    ),
    DIGITAL_CITIZEN(
        displayName = "Ciudadano Digital",
        description = "Comprendes la responsabilidad en línea, la huella digital y la ciberseguridad personal",
        requiredPhase = DigitalPhase.CREATIVE,
        requiredSkillIds = listOf("sec_04", "sec_05", "sec_06", "cont_03"),
        badgeColor = 0xFF7C4DFF, // Púrpura
        tier = 2
    ),
    CONTENT_CREATOR(
        displayName = "Creador de Contenido",
        description = "Sabes crear, editar y compartir contenido digital con responsabilidad",
        requiredPhase = DigitalPhase.CREATIVE,
        requiredSkillIds = listOf("cont_01", "cont_02", "cont_03"),
        badgeColor = 0xFFFF8C00, // Naranja
        tier = 2
    ),
    LOGIC_PROGRAMMER(
        displayName = "Programador Lógico",
        description = "Has desarrollado pensamiento computacional y creado tu primer proyecto",
        requiredPhase = DigitalPhase.CREATIVE,
        requiredSkillIds = listOf("prog_01", "prog_02", "prog_03", "prog_04"),
        badgeColor = 0xFF00BCD4, // Cian
        tier = 2
    ),
    CLOUD_NAVIGATOR(
        displayName = "Navegador de la Nube",
        description = "Dominas la nube, la búsqueda eficiente y el almacenamiento en línea",
        requiredPhase = DigitalPhase.CREATIVE,
        requiredSkillIds = listOf("web_03", "web_04"),
        badgeColor = 0xFF64B5F6, // Azul claro
        tier = 2
    ),
    DIGITAL_PROFESSIONAL(
        displayName = "Profesional Digital",
        description = "Manejas herramientas de productividad industrial y gestión de identidad profesional",
        requiredPhase = DigitalPhase.PROFESSIONAL,
        requiredSkillIds = listOf("prod_01", "prod_02", "prod_03"),
        badgeColor = 0xFFFFD700, // Dorado
        tier = 3
    ),
    AI_SPECIALIST(
        displayName = "Especialista en IA",
        description = "Comprendes la inteligencia artificial, su aplicación y su ética",
        requiredPhase = DigitalPhase.PROFESSIONAL,
        requiredSkillIds = listOf("ai_01", "ai_02", "ai_03"),
        badgeColor = 0xFFE040FB, // Magenta
        tier = 3
    ),
    FINANCE_MASTER(
        displayName = "Maestro de Finanzas Digitales",
        description = "Dominas la banca digital, e-commerce y conceptos de criptomonedas",
        requiredPhase = DigitalPhase.PROFESSIONAL,
        requiredSkillIds = listOf("fin_01", "fin_02", "fin_03"),
        badgeColor = 0xFF4CAF50, // Verde profundo
        tier = 3
    ),
    SECURITY_ARCHITECT(
        displayName = "Arquitecto de Seguridad",
        description = "Dominas autenticación avanzada, protección de datos y derechos digitales",
        requiredPhase = DigitalPhase.PROFESSIONAL,
        requiredSkillIds = listOf("sec_07", "sec_08"),
        badgeColor = 0xFFFF5252, // Rojo
        tier = 3
    ),
    DIGITAL_ARCHITECT(
        displayName = "Arquitecto Digital",
        description = "Has completado TODAS las competencias. Eres un profesional digital completo",
        requiredPhase = DigitalPhase.PROFESSIONAL,
        requiredSkillIds = listOf(), // Se verifica con todas las certificaciones anteriores
        badgeColor = 0xFFFFFFFF, // Blanco/Platino
        tier = 4
    )
}

/**
 * Registro de una certificación obtenida por el usuario.
 */
@Serializable
data class EarnedCertification(
    val type: CertificationType,
    val earnedAt: String,
    val scorePercent: Int = 100
)
