package com.liebeblack.isla_digital.domain.model

import kotlinx.serialization.Serializable
import java.time.Instant

/**
 * Entidad de dominio central que representa el perfil de un usuario en Isla Digital.
 * Versión 2.0 (2026): Soporta usuarios de 3 a 20 años con progresión por fases,
 * árbol de habilidades, certificaciones y modo acompañante.
 */
@Serializable
data class ChildProfile(
    val id: String,
    val name: String,
    val age: Int,
    val avatar: String,
    val createdAt: String,

    // === Fase y Progresión ===
    val totalPlayTimeMinutes: Int = 0,
    val currentLevel: Int = 1,
    val totalXp: Long = 0L,
    val streakDays: Int = 0,
    val lastActiveDate: String = "",

    // === Progreso de Habilidades Legacy (0-100) ===
    val logicProgress: Int = 0,
    val creativityProgress: Int = 0,
    val problemSolvingProgress: Int = 0,

    // === Árbol de Habilidades Digitales ===
    val skillProgress: Map<String, Int> = emptyMap(), // skillId -> xpEarned
    val completedSkillIds: List<String> = emptyList(),
    val unlockedSkillIds: List<String> = emptyList(),

    // === Certificaciones ===
    val earnedCertifications: List<EarnedCertification> = emptyList(),
    val earnedBadges: List<String> = emptyList(),

    // === Lecciones ===
    val completedLessonIds: List<String> = emptyList(),
    val currentLessonId: String? = null,
    val lessonsProgress: Map<String, Int> = emptyMap(), // lessonId -> percent

    // === Modo Acompañante ===
    val parentConfig: ParentConfig = ParentConfig(),

    // === Personalización ===
    val themeOverride: String? = null,
    val preferredLanguage: String = "es"
) {
    init {
        require(age in 3..20) { "La edad debe estar entre 3 y 20 años" }
        require(totalPlayTimeMinutes >= 0) { "El tiempo de juego no puede ser negativo" }
        require(currentLevel >= 1) { "El nivel actual debe ser al menos 1" }
    }

    /**
     * Calcula la fase actual basándose en la edad.
     */
    val currentPhase: DigitalPhase get() = DigitalPhase.fromAge(age)

    /**
     * Título honorífico basado en certificaciones.
     */
    val highestTitle: String get() {
        if (earnedCertifications.isEmpty()) return "Explorador Digital"
        return earnedCertifications
            .maxByOrNull { it.type.tier * 10 + it.type.ordinal }
            ?.type?.displayName ?: "Explorador"
    }

    // === Funciones de Progresión ===

    fun addPlayTime(minutes: Int): ChildProfile =
        copy(totalPlayTimeMinutes = totalPlayTimeMinutes + minutes)

    fun addXp(amount: Long): ChildProfile {
        val newXp = totalXp + amount
        var level = 1
        var threshold = 100L
        var accumulated = 0L
        while (accumulated + threshold <= newXp) {
            accumulated += threshold
            level++
            threshold = (100L * level * 1.2).toLong()
        }
        return copy(totalXp = newXp, currentLevel = level)
    }

    fun completeSkill(skillId: String): ChildProfile {
        if (skillId in completedSkillIds) return this
        val newCompleted = completedSkillIds + skillId
        val allSkills = SkillTreeData.getDefaultSkillTree()
        val newlyUnlocked = allSkills
            .filter { skill ->
                skill.prerequisiteIds.contains(skillId) &&
                skill.prerequisiteIds.all { it in newCompleted } &&
                skill.id !in unlockedSkillIds
            }
            .map { it.id }
        
        val profileWithSkills = copy(
            completedSkillIds = newCompleted,
            unlockedSkillIds = unlockedSkillIds + newlyUnlocked
        )
        
        return profileWithSkills.checkNewCertifications()
            .logActivity("Completó habilidad: $skillId", "Habilidades")
    }

    private fun checkNewCertifications(): ChildProfile {
        val earnedIds = earnedCertifications.map { it.type.name }.toSet()
        val newEarned = CertificationType.entries.filter { cert ->
            cert.name !in earnedIds && 
            cert.requiredSkillIds.isNotEmpty() &&
            cert.requiredSkillIds.all { it in completedSkillIds }
        }.map { type -> 
            EarnedCertification(type, java.time.Instant.now().toString())
        }
        
        // Certificación Final Especial (Arquitecto Digital)
        val allOtherCertsEarned = CertificationType.entries
            .filter { it != CertificationType.DIGITAL_ARCHITECT }
            .all { certType -> 
                (earnedCertifications.map { it.type } + newEarned.map { it.type }).contains(certType)
            }
        
        val finalCerts = if (allOtherCertsEarned && !earnedIds.contains(CertificationType.DIGITAL_ARCHITECT.name)) {
            newEarned + EarnedCertification(CertificationType.DIGITAL_ARCHITECT, java.time.Instant.now().toString())
        } else newEarned
        
        if (finalCerts.isEmpty()) return this
        
        return copy(earnedCertifications = earnedCertifications + finalCerts)
    }

    fun updateSkillXp(skillId: String, xp: Int): ChildProfile {
        val currentXp = skillProgress.getOrDefault(skillId, 0)
        return copy(skillProgress = skillProgress + (skillId to (currentXp + xp)))
    }

    fun awardBadge(badgeName: String): ChildProfile {
        if (earnedBadges.contains(badgeName)) return this
        val newBadges = earnedBadges + badgeName
        val levelUp = if (newBadges.size % 3 == 0) 1 else 0
        return copy(
            earnedBadges = newBadges,
            currentLevel = currentLevel + levelUp
        )
    }

    fun updateSkillProgress(logic: Int = 0, creativity: Int = 0, problemSolving: Int = 0): ChildProfile =
        copy(
            logicProgress = (logicProgress + logic).coerceIn(0, 100),
            creativityProgress = (creativityProgress + creativity).coerceIn(0, 100),
            problemSolvingProgress = (problemSolvingProgress + problemSolving).coerceIn(0, 100)
        )

    fun completeLesson(lessonId: String): ChildProfile {
        if (lessonId in completedLessonIds) return this
        val newProfile = copy(completedLessonIds = completedLessonIds + lessonId)
        return newProfile.logActivity("Completó lección: $lessonId", "Lecciones")
    }

    private fun logActivity(action: String, category: String, duration: Int = 0): ChildProfile {
        val entry = ActivityEntry(
            timestamp = java.time.Instant.now().toString(),
            action = action,
            category = category,
            durationMinutes = duration
        )
        val newLog = (parentConfig.activityLog + entry).takeLast(50)
        return copy(parentConfig = parentConfig.copy(activityLog = newLog))
    }

    companion object {
        fun createDefault(name: String = "Explorador", age: Int = 5): ChildProfile {
            val phase = DigitalPhase.fromAge(age)
            val initialSkills = SkillTreeData.getDefaultSkillTree()
                .filter { it.requiredPhase == phase && it.prerequisiteIds.isEmpty() }
                .map { it.id }

            return ChildProfile(
                id = "user_${System.currentTimeMillis()}",
                name = name,
                age = age,
                avatar = "avatar_base",
                createdAt = java.time.Instant.now().toString(),
                unlockedSkillIds = initialSkills
            )
        }
    }
}
