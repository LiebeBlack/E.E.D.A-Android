package com.liebeblack.isla_digital.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Face
import androidx.compose.material.icons.rounded.Palette
import androidx.compose.material.icons.rounded.Work
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.liebeblack.isla_digital.domain.model.DigitalPhase
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme

/**
 * Indicador visual de la fase actual del usuario.
 * Muestra el emoji, nombre y una barra de color suave.
 */
@Composable
fun PhaseIndicator(
    phase: DigitalPhase,
    modifier: Modifier = Modifier,
    compact: Boolean = false
) {
    val colors = IslaAdaptiveTheme.colors
    val config = IslaAdaptiveTheme.typoConfig

    val icon: ImageVector = when (phase) {
        DigitalPhase.SENSORIAL -> Icons.Rounded.Face
        DigitalPhase.CREATIVE -> Icons.Rounded.Palette
        DigitalPhase.PROFESSIONAL -> Icons.Rounded.Work
    }

    val gradientColors = listOf(colors.primary, colors.secondary)

    if (compact) {
        // Versión compacta: solo icono y nombre
        Row(
            modifier = modifier
                .clip(RoundedCornerShape(config.borderRadius.dp))
                .background(
                    brush = Brush.horizontalGradient(gradientColors.map { it.copy(alpha = 0.15f) })
                )
                .border(
                    width = 1.dp,
                    brush = Brush.horizontalGradient(gradientColors.map { it.copy(alpha = 0.3f) }),
                    shape = RoundedCornerShape(config.borderRadius.dp)
                )
                .padding(horizontal = 12.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = phase.displayName,
                tint = colors.primary,
                modifier = Modifier.size(16.dp)
            )
            Spacer(modifier = Modifier.width(6.dp))
            Text(
                text = phase.displayName,
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.Bold,
                    color = colors.primary
                )
            )
        }
    } else {
        // Versión completa: icono, nombre, descripción y barra
        Row(
            modifier = modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(config.borderRadius.dp))
                .background(
                    brush = Brush.horizontalGradient(gradientColors.map { it.copy(alpha = 0.1f) })
                )
                .border(
                    width = 1.dp,
                    brush = Brush.horizontalGradient(gradientColors.map { it.copy(alpha = 0.25f) }),
                    shape = RoundedCornerShape(config.borderRadius.dp)
                )
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Surface(
                modifier = Modifier.size(48.dp),
                shape = RoundedCornerShape(config.borderRadius.dp / 2),
                color = colors.primary.copy(alpha = 0.15f)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = icon,
                        contentDescription = null,
                        tint = colors.primary,
                        modifier = Modifier.size(28.dp)
                    )
                }
            }
            Spacer(modifier = Modifier.width(14.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "${phase.emoji} Fase ${phase.displayName}",
                    style = MaterialTheme.typography.titleSmall.copy(
                        fontWeight = FontWeight.Bold,
                        color = colors.onBackground
                    )
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = phase.description,
                    style = MaterialTheme.typography.bodySmall.copy(
                        color = colors.onBackground.copy(alpha = 0.7f)
                    )
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Edad: ${phase.ageRange.first}–${phase.ageRange.last} años",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = colors.primary,
                        fontWeight = FontWeight.SemiBold
                    )
                )
            }
        }
    }
}
