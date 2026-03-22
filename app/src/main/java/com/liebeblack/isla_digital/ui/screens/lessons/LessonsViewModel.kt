package com.liebeblack.isla_digital.ui.screens.lessons

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.liebeblack.isla_digital.domain.model.ChildProfile
import com.liebeblack.isla_digital.domain.model.DigitalPhase
import com.liebeblack.isla_digital.domain.repository.ChildProfileRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

/**
 * ViewModel para gestionar el progreso de las lecciones.
 * Filtra los módulos según la fase actual del perfil.
 */
class LessonsViewModel(
    private val repository: ChildProfileRepository
) : ViewModel() {

    val uiState: StateFlow<LessonsUiState> = repository.getProfile()
        .map { result ->
            val profile = result.getOrNull()
            if (profile != null) {
                val phase = profile.currentPhase
                LessonsUiState.Success(
                    phase = phase,
                    completedLessonIds = profile.completedLessonIds,
                    lessonsProgress = profile.lessonsProgress
                )
            } else {
                LessonsUiState.Error("No se pudo cargar el perfil.")
            }
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = LessonsUiState.Loading
        )

    fun completeLesson(lessonId: String) {
        viewModelScope.launch {
            repository.getProfile().first().getOrNull()?.let { profile ->
                val updated = profile.completeLesson(lessonId)
                repository.saveProfile(updated)
            }
        }
    }
}

sealed interface LessonsUiState {
    data object Loading : LessonsUiState
    data class Error(val message: String) : LessonsUiState
    data class Success(
        val phase: DigitalPhase,
        val completedLessonIds: List<String>,
        val lessonsProgress: Map<String, Int>
    ) : LessonsUiState
}
