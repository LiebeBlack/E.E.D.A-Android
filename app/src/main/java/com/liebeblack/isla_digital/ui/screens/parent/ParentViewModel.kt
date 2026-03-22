package com.liebeblack.isla_digital.ui.screens.parent

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.liebeblack.isla_digital.domain.model.*
import com.liebeblack.isla_digital.domain.repository.ChildProfileRepository
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch

/**
 * ViewModel para el Modo Acompañante (Parent Dashboard).
 * Gestiona autenticación PIN, límites y reporte de actividad.
 */
class ParentViewModel(
    private val repository: ChildProfileRepository
) : ViewModel() {

    private val _isAuthenticated = MutableStateFlow(false)
    val isAuthenticated: StateFlow<Boolean> = _isAuthenticated.asStateFlow()

    private val _pinError = MutableStateFlow(false)
    val pinError: StateFlow<Boolean> = _pinError.asStateFlow()

    val uiState: StateFlow<ParentUiState> = repository.getProfile()
        .map { result ->
            val profile = result.getOrNull()
            if (profile != null) {
                if (!profile.parentConfig.isEnabled || profile.parentConfig.parentPin.isEmpty()) {
                    _isAuthenticated.value = true
                }
                ParentUiState.Success(
                    config = profile.parentConfig,
                    childName = profile.name,
                    childAge = profile.age,
                    totalPlayTime = profile.totalPlayTimeMinutes
                )
            } else {
                ParentUiState.Error("No se encontró el perfil.")
            }
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = ParentUiState.Loading
        )

    fun authenticate(pin: String) {
        val state = uiState.value
        if (state is ParentUiState.Success) {
            if (state.config.isAccessible(pin)) {
                _isAuthenticated.value = true
                _pinError.value = false
            } else {
                _pinError.value = true
            }
        }
    }

    fun updateConfig(newConfig: ParentConfig) {
        viewModelScope.launch {
            repository.getProfile().first().getOrNull()?.let { profile ->
                repository.saveProfile(profile.copy(parentConfig = newConfig))
            }
        }
    }

    fun clearAuth() {
        _isAuthenticated.value = false
    }
}

sealed interface ParentUiState {
    data object Loading : ParentUiState
    data class Error(val message: String) : ParentUiState
    data class Success(
        val config: ParentConfig,
        val childName: String,
        val childAge: Int,
        val totalPlayTime: Int
    ) : ParentUiState
}
