package com.liebeblack.isla_digital.ui.screens.lessons

import androidx.compose.animation.*
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.liebeblack.isla_digital.domain.model.DigitalPhase
import com.liebeblack.isla_digital.ui.components.AdaptiveCard
import com.liebeblack.isla_digital.ui.components.MiniProgressRing
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme

data class LessonModule(
    val id: String, val title: String, val description: String,
    val icon: ImageVector, val phase: DigitalPhase,
    val totalLessons: Int, val completedLessons: Int = 0,
    val estimatedMinutes: Int = 15
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LessonsScreen(
    viewModel: LessonsViewModel,
    onNavigateBack: () -> Unit
) {
    val colors = IslaAdaptiveTheme.colors
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        containerColor = colors.background,
        topBar = {
            TopAppBar(
                title = { Text("📚 Lecciones", color = colors.onBackground, fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Rounded.ArrowBack, "Volver", tint = colors.onBackground)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = colors.background)
            )
        }
    ) { padding ->
        when (val state = uiState) {
            is LessonsUiState.Loading -> {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
            }
            is LessonsUiState.Error -> {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text(state.message, color = colors.error) }
            }
            is LessonsUiState.Success -> {
                val modules = remember(state.phase) { getLessonsForPhase(state.phase) }
                LazyColumn(
                    modifier = Modifier.fillMaxSize().padding(padding),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    item {
                        AdaptiveCard(modifier = Modifier.fillMaxWidth()) {
                            Column {
                                Text("${state.phase.emoji} Módulos — ${state.phase.displayName}",
                                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold, color = colors.onSurface))
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(state.phase.description, style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface.copy(alpha = 0.7f)))
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("${modules.size} módulos disponibles", style = MaterialTheme.typography.labelSmall.copy(color = colors.primary, fontWeight = FontWeight.SemiBold))
                            }
                        }
                    }
                    items(modules) { module -> 
                        val completedCount = if (module.id in state.completedLessonIds) module.totalLessons else 0
                        LessonModuleCard(
                            module = module.copy(completedLessons = completedCount),
                            onComplete = { viewModel.completeLesson(module.id) }
                        ) 
                    }
                    item { Spacer(modifier = Modifier.height(80.dp)) }
                }
            }
        }
    }
}

@Composable
private fun LessonModuleCard(
    module: LessonModule,
    onComplete: () -> Unit
) {
    val colors = IslaAdaptiveTheme.colors
    val config = IslaAdaptiveTheme.typoConfig
    val progress = if (module.totalLessons > 0) module.completedLessons.toFloat() / module.totalLessons else 0f

    AdaptiveCard(modifier = Modifier.fillMaxWidth().clickable { onComplete() }) {
        Row(modifier = Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Surface(Modifier.size(48.dp), shape = RoundedCornerShape(config.borderRadius.dp / 2), color = colors.primary.copy(alpha = 0.12f)) {
                Box(contentAlignment = Alignment.Center) { Icon(module.icon, null, tint = colors.primary, modifier = Modifier.size(26.dp)) }
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(module.title, style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold, color = colors.onSurface), maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(module.description, style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface.copy(alpha = 0.6f)), maxLines = 2, overflow = TextOverflow.Ellipsis)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Rounded.Timer, null, Modifier.size(14.dp), tint = colors.onSurface.copy(alpha = 0.5f))
                    Spacer(Modifier.width(4.dp))
                    Text("${module.estimatedMinutes} min · ${module.completedLessons}/${module.totalLessons}", style = MaterialTheme.typography.labelSmall.copy(color = colors.onSurface.copy(alpha = 0.5f)))
                }
            }
            MiniProgressRing(progress = progress, size = 36.dp)
        }
    }
}

private fun getLessonsForPhase(phase: DigitalPhase): List<LessonModule> = when (phase) {
    DigitalPhase.SENSORIAL -> listOf(
        LessonModule("s_01", "Toque y Gesto", "Interactúa con la pantalla táctil", Icons.Rounded.TouchApp, phase, 4, estimatedMinutes = 10),
        LessonModule("s_02", "Mis Botones", "Botones de tu dispositivo", Icons.Rounded.Smartphone, phase, 3, estimatedMinutes = 8),
        LessonModule("s_03", "Contraseña Mágica", "¿Qué es una contraseña?", Icons.Rounded.Lock, phase, 3, estimatedMinutes = 10),
        LessonModule("s_04", "Extraños en Pantalla", "Seguridad en internet", Icons.Rounded.Warning, phase, 4, estimatedMinutes = 12),
        LessonModule("s_05", "Iconos Mágicos", "WiFi, batería, cámara", Icons.Rounded.Apps, phase, 5, estimatedMinutes = 10),
        LessonModule("s_06", "¿Qué es Internet?", "La red del mundo", Icons.Rounded.Public, phase, 3, estimatedMinutes = 12),
        LessonModule("s_07", "Tiempo de Pantalla", "Uso saludable", Icons.Rounded.Timer, phase, 3, estimatedMinutes = 8),
        LessonModule("s_08", "Pedir Ayuda", "Cuándo pedir ayuda", Icons.Rounded.Favorite, phase, 2, estimatedMinutes = 8)
    )
    DigitalPhase.CREATIVE -> listOf(
        LessonModule("c_01", "Ciberseguridad", "Phishing y malware", Icons.Rounded.Security, phase, 5, estimatedMinutes = 20),
        LessonModule("c_02", "Huella Digital", "Todo deja rastro", Icons.Rounded.Fingerprint, phase, 4, estimatedMinutes = 15),
        LessonModule("c_03", "Contraseñas Fuertes", "Seguridad avanzada", Icons.Rounded.Key, phase, 4, estimatedMinutes = 15),
        LessonModule("c_04", "Pensamiento Lógico", "Resolver problemas", Icons.Rounded.Psychology, phase, 6, estimatedMinutes = 25),
        LessonModule("c_05", "Secuencias y Bucles", "Instrucciones repetidas", Icons.Rounded.Loop, phase, 5, estimatedMinutes = 20),
        LessonModule("c_06", "Variables y Datos", "Almacenar información", Icons.Rounded.Code, phase, 5, estimatedMinutes = 25),
        LessonModule("c_07", "Mi Primer Proyecto", "Tu primer programa", Icons.Rounded.RocketLaunch, phase, 8, estimatedMinutes = 40),
        LessonModule("c_08", "Foto y Edición", "Fotografía creativa", Icons.Rounded.PhotoCamera, phase, 4, estimatedMinutes = 15),
        LessonModule("c_09", "Video Creativo", "Edición de video", Icons.Rounded.Videocam, phase, 5, estimatedMinutes = 20),
        LessonModule("c_10", "Ciudadanía Digital", "Ética online", Icons.Rounded.People, phase, 4, estimatedMinutes = 15),
        LessonModule("c_11", "La Nube", "Almacenamiento cloud", Icons.Rounded.Cloud, phase, 4, estimatedMinutes = 15),
        LessonModule("c_12", "Búsqueda Eficiente", "Google y más", Icons.Rounded.Search, phase, 4, estimatedMinutes = 15)
    )
    DigitalPhase.PROFESSIONAL -> listOf(
        LessonModule("p_01", "¿Qué es la IA?", "Fundamentos de IA", Icons.Rounded.SmartToy, phase, 6, estimatedMinutes = 30),
        LessonModule("p_02", "IA Aplicada", "IA para productividad", Icons.Rounded.AutoAwesome, phase, 8, estimatedMinutes = 45),
        LessonModule("p_03", "Ética de Datos", "Privacidad y sesgo", Icons.Rounded.Balance, phase, 5, estimatedMinutes = 25),
        LessonModule("p_04", "Banca Digital", "Seguridad bancaria", Icons.Rounded.AccountBalance, phase, 5, estimatedMinutes = 25),
        LessonModule("p_05", "E-Commerce", "Compras seguras", Icons.Rounded.ShoppingCart, phase, 5, estimatedMinutes = 20),
        LessonModule("p_06", "Criptomonedas", "Blockchain básico", Icons.Rounded.CurrencyBitcoin, phase, 6, estimatedMinutes = 30),
        LessonModule("p_07", "Suite Ofimática", "Docs y hojas", Icons.Rounded.Description, phase, 8, estimatedMinutes = 40),
        LessonModule("p_08", "Gestión Proyectos", "Kanban y planning", Icons.Rounded.Dashboard, phase, 6, estimatedMinutes = 30),
        LessonModule("p_09", "Identidad Profesional", "LinkedIn y portafolio", Icons.Rounded.Badge, phase, 5, estimatedMinutes = 25),
        LessonModule("p_10", "Auth Avanzada", "2FA y biometría", Icons.Rounded.VerifiedUser, phase, 5, estimatedMinutes = 25),
        LessonModule("p_11", "Privacidad GDPR", "Derechos digitales", Icons.Rounded.Policy, phase, 5, estimatedMinutes = 25)
    )
}
