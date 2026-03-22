package com.liebeblack.isla_digital.ui.screens.certifications

import androidx.compose.animation.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.liebeblack.isla_digital.domain.model.CertificationType
import com.liebeblack.isla_digital.domain.model.EarnedCertification
import com.liebeblack.isla_digital.ui.components.AdaptiveCard
import com.liebeblack.isla_digital.ui.components.CertBadge
import com.liebeblack.isla_digital.ui.components.ProgressRing
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme

/**
 * Pantalla de Certificaciones.
 * Muestra el progreso hacia cada certificación y las ya obtenidas.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CertificationsScreen(
    earnedCertifications: List<EarnedCertification> = emptyList(),
    onNavigateBack: () -> Unit
) {
    val colors = IslaAdaptiveTheme.colors
    val config = IslaAdaptiveTheme.typoConfig
    val allCerts = CertificationType.entries.toList()
    val earnedTypes = earnedCertifications.map { it.type }
    val totalEarned = earnedCertifications.size
    val totalAvailable = allCerts.size
    val progress = if (totalAvailable > 0) totalEarned.toFloat() / totalAvailable else 0f

    Scaffold(
        containerColor = colors.background,
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        "🏆 Certificaciones",
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
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {
            // Resumen
            item {
                CertSummary(total = totalAvailable, earned = totalEarned, progress = progress)
            }

            // Certificaciones por tier
            (1..4).forEach { tier ->
                val tierCerts = allCerts.filter { it.tier == tier }
                if (tierCerts.isNotEmpty()) {
                    item {
                        TierSection(
                            tier = tier,
                            certifications = tierCerts,
                            earnedTypes = earnedTypes
                        )
                    }
                }
            }

            item { Spacer(modifier = Modifier.height(80.dp)) }
        }
    }
}

@Composable
private fun CertSummary(total: Int, earned: Int, progress: Float) {
    val colors = IslaAdaptiveTheme.colors

    AdaptiveCard(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            ProgressRing(
                progress = progress,
                size = 90.dp,
                strokeWidth = 8.dp,
                fillColor = colors.accent
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = "Certificaciones Digitales",
                    style = MaterialTheme.typography.titleMedium.copy(
                        fontWeight = FontWeight.Bold,
                        color = colors.onSurface
                    )
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "$earned de $total obtenidas",
                    style = MaterialTheme.typography.bodyMedium.copy(
                        color = colors.onSurface.copy(alpha = 0.7f)
                    )
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Completa habilidades para desbloquear más",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = colors.primary
                    )
                )
            }
        }
    }
}

@Composable
private fun TierSection(
    tier: Int,
    certifications: List<CertificationType>,
    earnedTypes: List<CertificationType>
) {
    val colors = IslaAdaptiveTheme.colors

    val tierLabel = when (tier) {
        1 -> "🥉 Tier 1 — Fundamentos"
        2 -> "🥈 Tier 2 — Creación"
        3 -> "🥇 Tier 3 — Profesional"
        4 -> "💎 Tier 4 — Maestría"
        else -> "Tier $tier"
    }

    Column {
        Text(
            text = tierLabel,
            style = MaterialTheme.typography.titleMedium.copy(
                fontWeight = FontWeight.Bold,
                color = colors.onBackground
            ),
            modifier = Modifier.padding(vertical = 8.dp)
        )

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            certifications.forEach { cert ->
                CertBadge(
                    certification = cert,
                    isEarned = cert in earnedTypes,
                    modifier = Modifier.weight(1f),
                    size = 80f
                )
            }
            // Fillers para mantener el grid alineado
            repeat((3 - certifications.size).coerceAtLeast(0)) {
                Spacer(modifier = Modifier.weight(1f))
            }
        }
    }
}
