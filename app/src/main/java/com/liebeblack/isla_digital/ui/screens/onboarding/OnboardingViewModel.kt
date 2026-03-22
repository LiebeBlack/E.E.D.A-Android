package com.liebeblack.isla_digital.ui.screens.onboarding

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.liebeblack.isla_digital.domain.model.ChildProfile
import com.liebeblack.isla_digital.domain.model.DigitalPhase
import com.liebeblack.isla_digital.domain.repository.ChildProfileRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class OnboardingViewModel(
    private val repository: ChildProfileRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(OnboardingUiState())
    val uiState: StateFlow<OnboardingUiState> = _uiState.asStateFlow()

    fun updateName(name: String) {
        _uiState.value = _uiState.value.copy(name = name)
    }

    fun updateAge(age: Int) {
        val phase = DigitalPhase.fromAge(age.coerceIn(3, 20))
        _uiState.value = _uiState.value.copy(
            age = age.coerceIn(3, 20),
            detectedPhase = phase
        )
    }

    fun selectAvatar(avatar: String) {
        _uiState.value = _uiState.value.copy(selectedAvatar = avatar)
    }

    fun nextStep() {
        val current = _uiState.value.currentStep
        if (current < 3) {
            _uiState.value = _uiState.value.copy(currentStep = current + 1)
        }
    }

    fun previousStep() {
        val current = _uiState.value.currentStep
        if (current > 0) {
            _uiState.value = _uiState.value.copy(currentStep = current - 1)
        }
    }

    fun completeOnboarding(onComplete: () -> Unit) {
        val state = _uiState.value
        if (!state.isValid) return

        _uiState.value = state.copy(isLoading = true)

        viewModelScope.launch {
            val profile = ChildProfile.createDefault(
                name = state.name,
                age = state.age
            ).copy(avatar = state.selectedAvatar)

            repository.saveProfile(profile)
            _uiState.value = state.copy(isLoading = false, isComplete = true)
            onComplete()
        }
    }
}

data class OnboardingUiState(
    val currentStep: Int = 0,
    val name: String = "",
    val age: Int = 5,
    val selectedAvatar: String = "avatar_base",
    val detectedPhase: DigitalPhase = DigitalPhase.SENSORIAL,
    val isLoading: Boolean = false,
    val isComplete: Boolean = false
) {
    val isValid: Boolean get() = name.isNotBlank() && age in 3..20
    val totalSteps: Int get() = 4
}
