package com.liebeblack.isla_digital.ui.screens.parent

import androidx.compose.animation.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
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
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.liebeblack.isla_digital.domain.model.ActivityEntry
import com.liebeblack.isla_digital.domain.model.ParentConfig
import com.liebeblack.isla_digital.ui.components.AdaptiveCard
import com.liebeblack.isla_digital.ui.components.ProgressRing
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ParentDashboardScreen(
    viewModel: ParentViewModel,
    onNavigateBack: () -> Unit
) {
    val colors = IslaAdaptiveTheme.colors
    val isAuthenticated by viewModel.isAuthenticated.collectAsState()
    val pinError by viewModel.pinError.collectAsState()
    val uiState by viewModel.uiState.collectAsState()
    var pinInput by remember { mutableStateOf("") }

    Scaffold(
        containerColor = colors.background,
        topBar = {
            TopAppBar(
                title = { Text("👨‍👩‍👧 Modo Acompañante", color = colors.onBackground, fontWeight = FontWeight.Bold) },
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
            is ParentUiState.Loading -> {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
            }
            is ParentUiState.Error -> {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text(state.message, color = colors.error) }
            }
            is ParentUiState.Success -> {
                if (!isAuthenticated) {
                    PinScreen(
                        pin = pinInput,
                        onPinChange = { pinInput = it },
                        onSubmit = { viewModel.authenticate(pinInput) },
                        showError = pinError,
                        modifier = Modifier.padding(padding)
                    )
                } else {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize().padding(padding),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        item { ChildSummaryCard(state.childName, state.childAge, state.totalPlayTime, state.config) }
                        item { TimeLimitCard(state.config) }
                        item { ContentFilterCard(state.config) }
                        item { ActivityLogCard(state.config.activityLog) }
                        item { PrivacyInfoCard() }
                        item { Spacer(modifier = Modifier.height(80.dp)) }
                    }
                }
            }
        }
    }
}

@Composable
private fun PinScreen(pin: String, onPinChange: (String) -> Unit, onSubmit: () -> Unit, showError: Boolean, modifier: Modifier) {
    val colors = IslaAdaptiveTheme.colors
    Column(modifier = modifier.fillMaxSize().padding(32.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
        Icon(Icons.Rounded.Lock, null, Modifier.size(64.dp), tint = colors.primary)
        Spacer(Modifier.height(16.dp))
        Text("Ingresa el PIN parental", style = MaterialTheme.typography.titleLarge.copy(color = colors.onBackground, fontWeight = FontWeight.Bold))
        Spacer(Modifier.height(24.dp))
        OutlinedTextField(
            value = pin, onValueChange = { if (it.length <= 6) onPinChange(it) },
            visualTransformation = PasswordVisualTransformation(),
            singleLine = true, shape = RoundedCornerShape(12.dp),
            isError = showError,
            supportingText = if (showError) {{ Text("PIN incorrecto", color = colors.error) }} else null,
            modifier = Modifier.width(200.dp)
        )
        Spacer(Modifier.height(16.dp))
        Button(onClick = onSubmit, shape = RoundedCornerShape(12.dp), colors = ButtonDefaults.buttonColors(containerColor = colors.primary)) { Text("Acceder") }
    }
}

@Composable
private fun ChildSummaryCard(name: String, age: Int, playTime: Int, config: ParentConfig) {
    val colors = IslaAdaptiveTheme.colors
    val timeProg = if (config.dailyTimeLimitMinutes > 0) playTime.toFloat() / config.dailyTimeLimitMinutes else 0f
    AdaptiveCard(Modifier.fillMaxWidth()) {
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            ProgressRing(progress = timeProg.coerceIn(0f, 1f), size = 70.dp, strokeWidth = 7.dp, fillColor = if (timeProg > 0.9f) colors.error else colors.primary)
            Spacer(Modifier.width(16.dp))
            Column {
                Text("📊 Resumen de $name", style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold, color = colors.onSurface))
                Text("Edad: $age años", style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface.copy(alpha = 0.7f)))
                Text("Tiempo hoy: $playTime / ${config.dailyTimeLimitMinutes} min", style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface.copy(alpha = 0.7f)))
                if (config.weeklyReportEnabled) Text("Reporte semanal: Activado", style = MaterialTheme.typography.labelSmall.copy(color = colors.success))
            }
        }
    }
}

@Composable
private fun TimeLimitCard(config: ParentConfig) {
    val colors = IslaAdaptiveTheme.colors
    AdaptiveCard(Modifier.fillMaxWidth()) {
        Column {
            DashInfoRow(Icons.Rounded.Timer, "Control de Tiempo", "Límite diario: ${config.dailyTimeLimitMinutes} minutos")
            Spacer(Modifier.height(4.dp))
            Text("Ajusta en Configuración > Modo Acompañante", style = MaterialTheme.typography.labelSmall.copy(color = colors.onSurface.copy(alpha = 0.5f)))
        }
    }
}

@Composable
private fun ContentFilterCard(config: ParentConfig) {
    val colors = IslaAdaptiveTheme.colors
    AdaptiveCard(Modifier.fillMaxWidth()) {
        Column {
            DashInfoRow(Icons.Rounded.FilterList, "Filtro de Contenido", config.contentFilterLevel.displayName)
            Spacer(Modifier.height(4.dp))
            Text("Controla qué contenido es accesible", style = MaterialTheme.typography.labelSmall.copy(color = colors.onSurface.copy(alpha = 0.5f)))
        }
    }
}

@Composable
private fun ActivityLogCard(log: List<ActivityEntry>) {
    val colors = IslaAdaptiveTheme.colors
    AdaptiveCard(Modifier.fillMaxWidth()) {
        Column {
            Text("📋 Log de Actividad", style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold, color = colors.onSurface))
            Spacer(Modifier.height(8.dp))
            if (log.isEmpty()) {
                Text("No hay actividad registrada aún.", style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface.copy(alpha = 0.5f)))
            } else {
                log.takeLast(5).reversed().forEach { entry ->
                    Row(Modifier.fillMaxWidth().padding(vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text("•", color = colors.primary, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.width(8.dp))
                        Column(Modifier.weight(1f)) {
                            Text(entry.action, style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface))
                            Text("${entry.category} · ${entry.durationMinutes} min", style = MaterialTheme.typography.labelSmall.copy(color = colors.onSurface.copy(alpha = 0.5f)))
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun PrivacyInfoCard() {
    val colors = IslaAdaptiveTheme.colors
    AdaptiveCard(Modifier.fillMaxWidth()) {
        Column {
            Text("🔐 Privacidad y Seguridad", style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold, color = colors.onSurface))
            Spacer(Modifier.height(8.dp))
            PrivacyItem("Datos almacenados solo en el dispositivo")
            PrivacyItem("Sin envío de datos externos")
            PrivacyItem("El hijo no ve monitoreo")
        }
    }
}

@Composable
private fun PrivacyItem(text: String) {
    val colors = IslaAdaptiveTheme.colors
    Row(Modifier.padding(vertical = 2.dp), verticalAlignment = Alignment.CenterVertically) {
        Icon(Icons.Rounded.CheckCircle, null, Modifier.size(16.dp), tint = colors.success)
        Spacer(Modifier.width(8.dp))
        Text(text, style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface.copy(alpha = 0.8f)))
    }
}

@Composable
private fun DashInfoRow(icon: ImageVector, title: String, value: String) {
    val colors = IslaAdaptiveTheme.colors
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, null, Modifier.size(24.dp), tint = colors.primary)
        Spacer(Modifier.width(12.dp))
        Column {
            Text(title, style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold, color = colors.onSurface))
            Text(value, style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface.copy(alpha = 0.7f)))
        }
    }
}
