package com.liebeblack.isla_digital.ui.screens.levels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.liebeblack.isla_digital.domain.model.DigitalPhase
import com.liebeblack.isla_digital.domain.repository.ChildProfileRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

sealed interface LevelsUiState {
    data object Loading : LevelsUiState
    data class Error(val message: String) : LevelsUiState
    data class Success(
        val currentLevel: Int,
        val totalXp: Long,
        val phase: DigitalPhase,
        val completedSkillIds: List<String>,
        val completedMapLevelIds: List<Int>
    ) : LevelsUiState
}

class LevelsViewModel(
    private val repository: ChildProfileRepository
) : ViewModel() {

    val uiState: StateFlow<LevelsUiState> = repository.getProfile()
        .map { result ->
            val profile = result.getOrNull()
            if (profile != null) {
                LevelsUiState.Success(
                    currentLevel = profile.currentLevel,
                    totalXp = profile.totalXp,
                    phase = profile.currentPhase,
                    completedSkillIds = profile.completedSkillIds,
                    completedMapLevelIds = profile.completedMapLevelIds
                )
            } else {
                LevelsUiState.Error("No se pudo cargar el perfil.")
            }
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = LevelsUiState.Loading
        )

    fun completeLevel(level: Level) {
        viewModelScope.launch {
            repository.getProfile().first().getOrNull()?.let { profile ->
                val updated = profile.finishMapLevel(level.id, level.xpReward)
                repository.saveProfile(updated)
            }
        }
    }
}
