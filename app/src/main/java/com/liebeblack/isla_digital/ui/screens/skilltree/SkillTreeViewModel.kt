package com.liebeblack.isla_digital.ui.screens.skilltree

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.liebeblack.isla_digital.domain.model.*
import com.liebeblack.isla_digital.domain.repository.ChildProfileRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

/**
 * ViewModel para la pantalla del Árbol de Habilidades.
 * Gestiona el filtrado y el progreso real del usuario.
 */
class SkillTreeViewModel(
    private val repository: ChildProfileRepository
) : ViewModel() {

    private val _selectedCategory = MutableStateFlow<SkillCategory?>(null)
    private val _selectedSkillId = MutableStateFlow<String?>(null)

    val uiState: StateFlow<SkillTreeUiState> = combine(
        repository.getProfile(),
        _selectedCategory,
        _selectedSkillId
    ) { profileResult, category, skillId ->
        val profile = profileResult.getOrNull()
        val allSkills = SkillTreeData.getDefaultSkillTree()
        val categories = SkillCategory.entries.toList()
        
        val filtered = if (category != null) {
            allSkills.filter { it.category == category }
        } else {
            allSkills
        }

        SkillTreeUiState(
            allSkills = allSkills,
            categories = categories,
            selectedCategory = category,
            filteredSkills = filtered,
            selectedSkillId = skillId,
            completedSkillIds = profile?.completedSkillIds ?: emptyList(),
            unlockedSkillIds = profile?.unlockedSkillIds ?: emptyList(),
            skillProgress = profile?.skillProgress ?: emptyMap()
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = SkillTreeUiState()
    )

    fun selectCategory(category: SkillCategory?) {
        _selectedCategory.value = category
    }

    fun selectSkill(skillId: String) {
        _selectedSkillId.value = if (skillId.isEmpty()) null else skillId
    }

    fun clearSelection() {
        _selectedSkillId.value = null
    }

    fun unlockSkill(skillId: String) {
        viewModelScope.launch {
            repository.getProfile().first().getOrNull()?.let { profile ->
                val updated = profile.completeSkill(skillId)
                repository.saveProfile(updated)
            }
        }
    }
}

data class SkillTreeUiState(
    val allSkills: List<SkillNode> = emptyList(),
    val categories: List<SkillCategory> = emptyList(),
    val selectedCategory: SkillCategory? = null,
    val filteredSkills: List<SkillNode> = emptyList(),
    val selectedSkillId: String? = null,
    val completedSkillIds: List<String> = emptyList(),
    val unlockedSkillIds: List<String> = emptyList(),
    val skillProgress: Map<String, Int> = emptyMap()
) {
    val selectedSkill: SkillNode?
        get() = allSkills.find { it.id == selectedSkillId }
}
