package com.liebeblack.isla_digital.domain.model

import kotlinx.serialization.Serializable

/**
 * Categorías del Árbol de Habilidades Digitales.
 */
@Serializable
enum class SkillCategory(val displayName: String, val icon: String) {
    SECURITY("Seguridad Digital", "shield"),
    DEVICE_TOOLS("Herramientas del Dispositivo", "phone_android"),
    WEB_NAVIGATION("Navegación y Web", "language"),
    PROGRAMMING("Programación y Lógica", "code"),
    CONTENT_CREATION("Creación de Contenido", "palette"),
    AI_TECH("IA y Tecnologías Emergentes", "smart_toy"),
    DIGITAL_FINANCE("Finanzas Digitales", "account_balance"),
    PRODUCTIVITY("Productividad", "dashboard")
}

/**
 * Un nodo individual dentro del Árbol de Habilidades Digitales.
 * Representa una competencia específica que el usuario puede desbloquear.
 */
@Serializable
data class SkillNode(
    val id: String,
    val name: String,
    val description: String,
    val category: SkillCategory,
    val requiredPhase: DigitalPhase,
    val xpRequired: Int = 100,
    val xpEarned: Int = 0,
    val isUnlocked: Boolean = false,
    val isCompleted: Boolean = false,
    val prerequisiteIds: List<String> = emptyList(),
    val tier: Int = 1 // 1-5, nivel de profundidad dentro de la categoría
) {
    val progressPercent: Float
        get() = if (xpRequired > 0) (xpEarned.toFloat() / xpRequired).coerceIn(0f, 1f) else 0f
}

/**
 * Árbol completo de habilidades con datos predefinidos por fase.
 */
object SkillTreeData {

    fun getDefaultSkillTree(): List<SkillNode> = buildList {
        // === FASE SENSORIAL (3-7 años) ===
        // Seguridad Digital
        add(SkillNode("sec_01", "Contraseña Mágica", "Aprende qué es una contraseña y por qué no la debes compartir", SkillCategory.SECURITY, DigitalPhase.SENSORIAL, 50, tier = 1))
        add(SkillNode("sec_02", "Extraños en la Pantalla", "Identifica cuándo alguien desconocido intenta hablar contigo", SkillCategory.SECURITY, DigitalPhase.SENSORIAL, 60, tier = 1))
        add(SkillNode("sec_03", "Pedir Ayuda", "Sabe cuándo pedirle ayuda a un adulto de confianza", SkillCategory.SECURITY, DigitalPhase.SENSORIAL, 50, tier = 1, prerequisiteIds = listOf("sec_01")))

        // Herramientas del Dispositivo
        add(SkillNode("dev_01", "Toque y Gesto", "Domina los gestos básicos: tocar, deslizar, pellizcar", SkillCategory.DEVICE_TOOLS, DigitalPhase.SENSORIAL, 40, tier = 1))
        add(SkillNode("dev_02", "Mis Botones", "Identifica los botones de inicio, volumen y bloqueo", SkillCategory.DEVICE_TOOLS, DigitalPhase.SENSORIAL, 50, tier = 1))
        add(SkillNode("dev_03", "Tiempo de Pantalla", "Entiende la importancia de descansar los ojos", SkillCategory.DEVICE_TOOLS, DigitalPhase.SENSORIAL, 40, tier = 1))

        // Navegación Web
        add(SkillNode("web_01", "¿Qué es Internet?", "Comprende Internet como una red de información", SkillCategory.WEB_NAVIGATION, DigitalPhase.SENSORIAL, 60, tier = 1))
        add(SkillNode("web_02", "Iconos Mágicos", "Reconoce iconos comunes: WiFi, batería, cámara", SkillCategory.WEB_NAVIGATION, DigitalPhase.SENSORIAL, 40, tier = 1))

        // === FASE CREATIVA (8-14 años) ===
        // Seguridad Digital Avanzada
        add(SkillNode("sec_04", "Ciberseguridad Personal", "Aprende sobre phishing, malware y cómo protegerte", SkillCategory.SECURITY, DigitalPhase.CREATIVE, 100, tier = 2, prerequisiteIds = listOf("sec_03")))
        add(SkillNode("sec_05", "Huella Digital", "Entiende que todo lo que publicas deja rastro", SkillCategory.SECURITY, DigitalPhase.CREATIVE, 80, tier = 2))
        add(SkillNode("sec_06", "Contraseñas Fuertes", "Crea contraseñas seguras y usa gestores", SkillCategory.SECURITY, DigitalPhase.CREATIVE, 100, tier = 2, prerequisiteIds = listOf("sec_04")))

        // Programación y Lógica
        add(SkillNode("prog_01", "Pensamiento Lógico", "Descomponer problemas en pasos simples", SkillCategory.PROGRAMMING, DigitalPhase.CREATIVE, 80, tier = 2))
        add(SkillNode("prog_02", "Secuencias y Bucles", "Instrucciones paso a paso y repeticiones", SkillCategory.PROGRAMMING, DigitalPhase.CREATIVE, 100, tier = 2, prerequisiteIds = listOf("prog_01")))
        add(SkillNode("prog_03", "Variables y Datos", "Almacenar y transformar información", SkillCategory.PROGRAMMING, DigitalPhase.CREATIVE, 120, tier = 3, prerequisiteIds = listOf("prog_02")))
        add(SkillNode("prog_04", "Mi Primer Proyecto", "Crea tu primer mini-programa interactivo", SkillCategory.PROGRAMMING, DigitalPhase.CREATIVE, 150, tier = 3, prerequisiteIds = listOf("prog_03")))

        // Creación de Contenido
        add(SkillNode("cont_01", "Foto y Edición", "Toma fotos y aplica ediciones básicas", SkillCategory.CONTENT_CREATION, DigitalPhase.CREATIVE, 80, tier = 2))
        add(SkillNode("cont_02", "Video Creativo", "Graba y edita videos cortos con mensaje", SkillCategory.CONTENT_CREATION, DigitalPhase.CREATIVE, 100, tier = 2, prerequisiteIds = listOf("cont_01")))
        add(SkillNode("cont_03", "Ciudadanía Digital", "Respeto, empatía y responsabilidad en línea", SkillCategory.CONTENT_CREATION, DigitalPhase.CREATIVE, 80, tier = 2))

        // Navegación Web Avanzada
        add(SkillNode("web_03", "La Nube", "Almacenar, sincronizar y compartir archivos en la nube", SkillCategory.WEB_NAVIGATION, DigitalPhase.CREATIVE, 100, tier = 2, prerequisiteIds = listOf("web_01", "web_02")))
        add(SkillNode("web_04", "Búsqueda Eficiente", "Usa motores de búsqueda de forma efectiva y crítica", SkillCategory.WEB_NAVIGATION, DigitalPhase.CREATIVE, 80, tier = 2))

        // === FASE PROFESIONAL (15-20 años) ===
        // IA y Tecnologías Emergentes
        add(SkillNode("ai_01", "¿Qué es la IA?", "Comprende los fundamentos de la inteligencia artificial", SkillCategory.AI_TECH, DigitalPhase.PROFESSIONAL, 120, tier = 3))
        add(SkillNode("ai_02", "IA Aplicada", "Usa herramientas de IA para productividad real", SkillCategory.AI_TECH, DigitalPhase.PROFESSIONAL, 150, tier = 4, prerequisiteIds = listOf("ai_01")))
        add(SkillNode("ai_03", "Ética de Datos", "Privacidad, sesgo algorítmico y responsabilidad", SkillCategory.AI_TECH, DigitalPhase.PROFESSIONAL, 100, tier = 4, prerequisiteIds = listOf("ai_01")))

        // Finanzas Digitales
        add(SkillNode("fin_01", "Banca Digital", "Entiende cuentas, transferencias y seguridad bancaria", SkillCategory.DIGITAL_FINANCE, DigitalPhase.PROFESSIONAL, 120, tier = 3))
        add(SkillNode("fin_02", "E-Commerce", "Compras en línea seguras y derechos del consumidor", SkillCategory.DIGITAL_FINANCE, DigitalPhase.PROFESSIONAL, 100, tier = 3, prerequisiteIds = listOf("fin_01")))
        add(SkillNode("fin_03", "Criptomonedas Básicas", "Conceptos básicos de blockchain y monedas digitales", SkillCategory.DIGITAL_FINANCE, DigitalPhase.PROFESSIONAL, 150, tier = 4, prerequisiteIds = listOf("fin_02")))

        // Productividad
        add(SkillNode("prod_01", "Suite Ofimática", "Domina documentos, hojas de cálculo y presentaciones", SkillCategory.PRODUCTIVITY, DigitalPhase.PROFESSIONAL, 100, tier = 3))
        add(SkillNode("prod_02", "Gestión de Proyectos", "Herramientas como Kanban, calendarios y planificación", SkillCategory.PRODUCTIVITY, DigitalPhase.PROFESSIONAL, 120, tier = 4, prerequisiteIds = listOf("prod_01")))
        add(SkillNode("prod_03", "Identidad Profesional", "LinkedIn, portafolio digital y marca personal", SkillCategory.PRODUCTIVITY, DigitalPhase.PROFESSIONAL, 120, tier = 4))

        // Seguridad Profesional
        add(SkillNode("sec_07", "Autenticación Avanzada", "2FA, biometría y seguridad empresarial", SkillCategory.SECURITY, DigitalPhase.PROFESSIONAL, 120, tier = 4, prerequisiteIds = listOf("sec_06")))
        add(SkillNode("sec_08", "Privacidad de Datos", "GDPR, derechos digitales y protección de información", SkillCategory.SECURITY, DigitalPhase.PROFESSIONAL, 100, tier = 4, prerequisiteIds = listOf("sec_07")))
    }
}
