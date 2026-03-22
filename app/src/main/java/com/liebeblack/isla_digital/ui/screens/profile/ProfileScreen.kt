package com.liebeblack.isla_digital.ui.screens.profile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.liebeblack.isla_digital.domain.model.ChildProfile
import com.liebeblack.isla_digital.domain.model.DigitalPhase
import com.liebeblack.isla_digital.ui.components.AdaptiveCard
import com.liebeblack.isla_digital.ui.components.PhaseIndicator
import com.liebeblack.isla_digital.ui.components.ProgressRing
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme

@Suppress("DEPRECATION")
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(profile: ChildProfile?, onNavigateBack: () -> Unit) {
    val colors = IslaAdaptiveTheme.colors
    val phase = if (profile != null) DigitalPhase.fromAge(profile.age) else DigitalPhase.SENSORIAL

    Scaffold(
        containerColor = colors.background,
        topBar = {
            TopAppBar(
                title = { Text("👤 Perfil", color = colors.onBackground, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) { Icon(Icons.AutoMirrored.Rounded.ArrowBack, "Volver", tint = colors.onBackground) }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = colors.background)
            )
        }
    ) { padding ->
        if (profile == null) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("No se encontró el perfil.", color = colors.onBackground)
            }
            return@Scaffold
        }

        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Avatar y nombre
            item {
                AdaptiveCard(Modifier.fillMaxWidth()) {
                    Column(Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
                        Surface(Modifier.size(80.dp), shape = CircleShape, color = colors.primary.copy(alpha = 0.15f)) {
                            Box(contentAlignment = Alignment.Center) {
                                when (profile.avatar) {
                                    "avatar_explorer" -> Icon(Icons.Rounded.Explore, null, Modifier.size(48.dp), tint = colors.primary)
                                    "avatar_star" -> Icon(Icons.Rounded.Star, null, Modifier.size(48.dp), tint = colors.primary)
                                    "avatar_rocket" -> Icon(Icons.Rounded.RocketLaunch, null, Modifier.size(48.dp), tint = colors.primary)
                                    "avatar_nature" -> Icon(Icons.Rounded.Park, null, Modifier.size(48.dp), tint = colors.primary)
                                    "avatar_music" -> Icon(Icons.Rounded.MusicNote, null, Modifier.size(48.dp), tint = colors.primary)
                                    "avatar_science" -> Icon(Icons.Rounded.Science, null, Modifier.size(48.dp), tint = colors.primary)
                                    else -> Icon(Icons.Rounded.Face, null, Modifier.size(48.dp), tint = colors.primary)
                                }
                            }
                        }
                        Spacer(Modifier.height(12.dp))
                        Text(profile.name, style = MaterialTheme.typography.headlineSmall.copy(fontWeight = FontWeight.Bold, color = colors.onSurface))
                        Text("Nivel ${profile.currentLevel} • ${profile.age} años", style = MaterialTheme.typography.bodyMedium.copy(color = colors.onSurface.copy(alpha = 0.6f)))
                        Spacer(Modifier.height(8.dp))
                        PhaseIndicator(phase = phase, compact = true)
                    }
                }
            }

            // Estadísticas
            item {
                AdaptiveCard(Modifier.fillMaxWidth()) {
                    Column {
                        Text("📊 Estadísticas", style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold, color = colors.onSurface))
                        Spacer(Modifier.height(12.dp))
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceEvenly) {
                            StatItem("Lógica", profile.logicProgress, colors.primary)
                            StatItem("Creatividad", profile.creativityProgress, colors.secondary)
                            StatItem("Problemas", profile.problemSolvingProgress, colors.accent)
                        }
                    }
                }
            }

            // Info general
            item {
                AdaptiveCard(Modifier.fillMaxWidth()) {
                    Column {
                        Text("📋 Información", style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold, color = colors.onSurface))
                        Spacer(Modifier.height(8.dp))
                        InfoRow(Icons.Rounded.Timer, "Tiempo de juego", "${profile.totalPlayTimeMinutes} minutos")
                        InfoRow(Icons.Rounded.Star, "Medallas", "${profile.earnedBadges.size} obtenidas")
                        InfoRow(Icons.Rounded.TrendingUp, "Nivel", "${profile.currentLevel}")
                        InfoRow(Icons.Rounded.CalendarToday, "Creado", profile.createdAt.take(10))
                    }
                }
            }

            item { Spacer(Modifier.height(80.dp)) }
        }
    }
}

@Composable
private fun StatItem(label: String, progress: Int, color: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        ProgressRing(progress = progress / 100f, size = 60.dp, strokeWidth = 6.dp, fillColor = color)
        Spacer(Modifier.height(4.dp))
        Text(label, style = MaterialTheme.typography.labelSmall.copy(color = IslaAdaptiveTheme.colors.onSurface.copy(alpha = 0.7f)))
    }
}

@Composable
private fun InfoRow(icon: ImageVector, label: String, value: String) {
    val colors = IslaAdaptiveTheme.colors
    Row(Modifier.fillMaxWidth().padding(vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, null, Modifier.size(20.dp), tint = colors.primary)
        Spacer(Modifier.width(12.dp))
        Text(label, Modifier.weight(1f), style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface.copy(alpha = 0.7f)))
        Text(value, style = MaterialTheme.typography.bodySmall.copy(fontWeight = FontWeight.SemiBold, color = colors.onSurface))
    }
}
