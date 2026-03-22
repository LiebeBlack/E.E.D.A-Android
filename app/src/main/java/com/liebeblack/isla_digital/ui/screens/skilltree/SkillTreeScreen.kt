package com.liebeblack.isla_digital.ui.screens.skilltree

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.liebeblack.isla_digital.domain.model.DigitalPhase
import com.liebeblack.isla_digital.domain.model.SkillCategory
import com.liebeblack.isla_digital.domain.model.SkillNode
import com.liebeblack.isla_digital.ui.components.AdaptiveCard
import com.liebeblack.isla_digital.ui.components.ProgressRing
import com.liebeblack.isla_digital.ui.components.SkillTreeNodeView
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme

/**
 * Pantalla del Árbol de Habilidades Digitales.
 * Muestra las habilidades organizadas por categoría con progreso visual.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SkillTreeScreen(
    uiState: SkillTreeUiState,
    onCategorySelected: (SkillCategory?) -> Unit,
    onSkillSelected: (String) -> Unit,
    onUnlockSkill: (String) -> Unit,
    onNavigateBack: () -> Unit
) {
    val colors = IslaAdaptiveTheme.colors
    val config = IslaAdaptiveTheme.typoConfig

    Scaffold(
        containerColor = colors.background,
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        "🌳 Árbol de Habilidades",
                        color = colors.onBackground,
                        fontWeight = FontWeight.Bold
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            Icons.AutoMirrored.Rounded.ArrowBack,
                            contentDescription = "Volver",
                            tint = colors.onBackground
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = colors.background
                )
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Resumen de progreso
            item {
                SkillTreeSummary(uiState = uiState)
            }

            // Filtros de categoría
            item {
                CategoryFilter(
                    categories = uiState.categories,
                    selectedCategory = uiState.selectedCategory,
                    onCategorySelected = onCategorySelected
                )
            }

            // Habilidades agrupadas por fase
            DigitalPhase.entries.forEach { phase ->
                val phaseSkills = uiState.filteredSkills.filter { it.requiredPhase == phase }
                if (phaseSkills.isNotEmpty()) {
                    item {
                        PhaseSection(
                            phase = phase,
                            skills = phaseSkills,
                            completedIds = uiState.completedSkillIds,
                            unlockedIds = uiState.unlockedSkillIds,
                            skillProgress = uiState.skillProgress,
                            onSkillSelected = onSkillSelected
                        )
                    }
                }
            }

            item { Spacer(modifier = Modifier.height(80.dp)) }
        }

        // Detalle del skill seleccionado
        uiState.selectedSkill?.let { skill ->
            SkillDetailSheet(
                skill = skill,
                isCompleted = skill.id in uiState.completedSkillIds,
                isUnlocked = skill.id in uiState.unlockedSkillIds,
                xpEarned = uiState.skillProgress[skill.id] ?: 0,
                onUnlock = { 
                    onUnlockSkill(skill.id)
                    onSkillSelected("") 
                },
                onDismiss = { onSkillSelected("") }
            )
        }
    }
}

@Composable
private fun SkillTreeSummary(uiState: SkillTreeUiState) {
    val colors = IslaAdaptiveTheme.colors
    val totalSkills = uiState.allSkills.size
    val completed = uiState.completedSkillIds.size
    val progress = if (totalSkills > 0) completed.toFloat() / totalSkills else 0f

    AdaptiveCard(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            ProgressRing(
                progress = progress,
                size = 80.dp,
                strokeWidth = 8.dp
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = "Progreso General",
                    style = MaterialTheme.typography.titleMedium.copy(
                        fontWeight = FontWeight.Bold,
                        color = colors.onSurface
                    )
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "$completed de $totalSkills habilidades completadas",
                    style = MaterialTheme.typography.bodyMedium.copy(
                        color = colors.onSurface.copy(alpha = 0.7f)
                    )
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "${uiState.categories.size} categorías disponibles",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = colors.primary
                    )
                )
            }
        }
    }
}

@Composable
private fun CategoryFilter(
    categories: List<SkillCategory>,
    selectedCategory: SkillCategory?,
    onCategorySelected: (SkillCategory?) -> Unit
) {
    val colors = IslaAdaptiveTheme.colors
    val config = IslaAdaptiveTheme.typoConfig

    LazyRow(
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // "Todas" chip
        item {
            FilterChip(
                selected = selectedCategory == null,
                onClick = { onCategorySelected(null) },
                label = { Text("Todas") },
                colors = FilterChipDefaults.filterChipColors(
                    selectedContainerColor = colors.primary.copy(alpha = 0.15f),
                    selectedLabelColor = colors.primary
                ),
                shape = RoundedCornerShape(config.borderRadius.dp)
            )
        }

        items(categories) { category ->
            FilterChip(
                selected = selectedCategory == category,
                onClick = { onCategorySelected(category) },
                label = { Text(category.displayName, maxLines = 1) },
                colors = FilterChipDefaults.filterChipColors(
                    selectedContainerColor = colors.primary.copy(alpha = 0.15f),
                    selectedLabelColor = colors.primary
                ),
                shape = RoundedCornerShape(config.borderRadius.dp)
            )
        }
    }
}

@Composable
private fun PhaseSection(
    phase: DigitalPhase,
    skills: List<SkillNode>,
    completedIds: List<String>,
    unlockedIds: List<String>,
    skillProgress: Map<String, Int>,
    onSkillSelected: (String) -> Unit
) {
    val colors = IslaAdaptiveTheme.colors

    Column {
        // Header de fase
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(vertical = 8.dp)
        ) {
            Text(
                text = "${phase.emoji} ${phase.displayName}",
                style = MaterialTheme.typography.titleMedium.copy(
                    fontWeight = FontWeight.Bold,
                    color = colors.onBackground
                )
            )
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = "(${phase.ageRange.first}-${phase.ageRange.last} años)",
                style = MaterialTheme.typography.labelSmall.copy(
                    color = colors.onBackground.copy(alpha = 0.5f)
                )
            )
        }

        // Grid de habilidades en LazyRow
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(skills) { skill ->
                SkillTreeNodeView(
                    skillNode = skill,
                    isUnlocked = skill.id in unlockedIds || skill.prerequisiteIds.isEmpty(),
                    isCompleted = skill.id in completedIds,
                    xpEarned = skillProgress[skill.id] ?: 0,
                    onClick = { onSkillSelected(skill.id) }
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun SkillDetailSheet(
    skill: SkillNode,
    isCompleted: Boolean,
    isUnlocked: Boolean,
    xpEarned: Int,
    onUnlock: () -> Unit,
    onDismiss: () -> Unit
) {
    val colors = IslaAdaptiveTheme.colors

    AlertDialog(
        onDismissRequest = onDismiss,
        containerColor = colors.surface,
        title = {
            Text(
                text = skill.name,
                style = MaterialTheme.typography.titleLarge.copy(
                    fontWeight = FontWeight.Bold,
                    color = colors.onSurface
                )
            )
        },
        text = {
            Column {
                Text(
                    text = skill.description,
                    style = MaterialTheme.typography.bodyMedium.copy(
                        color = colors.onSurface.copy(alpha = 0.8f)
                    )
                )
                Spacer(modifier = Modifier.height(12.dp))
                Row {
                    Text("Categoría: ", fontWeight = FontWeight.SemiBold, color = colors.onSurface)
                    Text(skill.category.displayName, color = colors.primary)
                }
                Row {
                    Text("Fase: ", fontWeight = FontWeight.SemiBold, color = colors.onSurface)
                    Text("${skill.requiredPhase.emoji} ${skill.requiredPhase.displayName}", color = colors.onSurface)
                }
                Row {
                    Text("Tier: ", fontWeight = FontWeight.SemiBold, color = colors.onSurface)
                    Text("${skill.tier}", color = colors.onSurface)
                }
                Row {
                    Text("XP: ", fontWeight = FontWeight.SemiBold, color = colors.onSurface)
                    Text("$xpEarned / ${skill.xpRequired}", color = colors.primary)
                }
                if (isCompleted) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        "✅ Habilidad completada",
                        color = colors.success,
                        fontWeight = FontWeight.Bold
                    )
                } else if (!isUnlocked) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        "🔒 Requisitos previos pendientes",
                        color = colors.warning,
                        fontWeight = FontWeight.Medium
                    )
                }
            }
        },
        confirmButton = {
            if (isUnlocked && !isCompleted) {
                Button(
                    onClick = onUnlock,
                    colors = ButtonDefaults.buttonColors(containerColor = colors.primary)
                ) {
                    Text("Completar Habilidad")
                }
            } else {
                TextButton(onClick = onDismiss) {
                    Text("Cerrar", color = colors.primary)
                }
            }
        },
        dismissButton = {
            if (isUnlocked && !isCompleted) {
                TextButton(onClick = onDismiss) {
                    Text("Cancelar", color = colors.onSurface.copy(alpha = 0.5f))
                }
            }
        }
    )
}
