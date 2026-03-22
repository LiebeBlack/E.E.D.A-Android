package com.liebeblack.isla_digital.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Fill
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.liebeblack.isla_digital.domain.model.CertificationType
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

/**
 * Badge hexagonal de certificación con efecto de brillo animado.
 * Muestra el nombre y tier de la certificación con el color correspondiente.
 */
@Composable
fun CertBadge(
    certification: CertificationType,
    isEarned: Boolean,
    modifier: Modifier = Modifier,
    size: Float = 100f
) {
    val badgeColor = if (isEarned) Color(certification.badgeColor) else Color.Gray.copy(alpha = 0.4f)
    val colors = IslaAdaptiveTheme.colors

    // Animación de brillo sutil para badges ganadas
    val infiniteTransition = rememberInfiniteTransition(label = "badgeGlow")
    val glowAlpha by if (isEarned) {
        infiniteTransition.animateFloat(
            initialValue = 0.3f,
            targetValue = 0.7f,
            animationSpec = infiniteRepeatable(
                animation = tween(2000, easing = FastOutSlowInEasing),
                repeatMode = RepeatMode.Reverse
            ),
            label = "glowPulse"
        )
    } else {
        remember { mutableFloatStateOf(0f) }
    }

    val rotation by if (isEarned && certification.tier == 4) {
        infiniteTransition.animateFloat(
            initialValue = 0f,
            targetValue = 360f,
            animationSpec = infiniteRepeatable(
                animation = tween(8000, easing = LinearEasing)
            ),
            label = "badgeRotation"
        )
    } else {
        remember { mutableFloatStateOf(0f) }
    }

    Column(
        modifier = modifier.width(size.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(
            modifier = Modifier.size(size.dp),
            contentAlignment = Alignment.Center
        ) {
            // Resplandor de fondo
            if (isEarned) {
                Box(
                    modifier = Modifier
                        .size((size * 1.15f).dp)
                        .clip(CircleShape)
                        .background(
                            brush = Brush.radialGradient(
                                colors = listOf(
                                    badgeColor.copy(alpha = glowAlpha * 0.4f),
                                    Color.Transparent
                                )
                            )
                        )
                )
            }

            // Hexágono
            Canvas(
                modifier = Modifier
                    .size(size.dp)
                    .then(
                        if (certification.tier == 4 && isEarned) {
                            Modifier.rotate(rotation)
                        } else Modifier
                    )
            ) {
                val centerX = this.size.width / 2
                val centerY = this.size.height / 2
                val radius = this.size.minDimension / 2 * 0.85f

                val hexPath = Path().apply {
                    for (i in 0..5) {
                        val angle = (PI / 3 * i - PI / 2).toFloat()
                        val x = centerX + radius * cos(angle)
                        val y = centerY + radius * sin(angle)
                        if (i == 0) moveTo(x, y) else lineTo(x, y)
                    }
                    close()
                }

                drawPath(
                    path = hexPath,
                    color = if (isEarned) badgeColor else Color.Gray.copy(alpha = 0.2f),
                    style = Fill
                )

                // Borde interior más claro
                val innerRadius = radius * 0.75f
                val innerPath = Path().apply {
                    for (i in 0..5) {
                        val angle = (PI / 3 * i - PI / 2).toFloat()
                        val x = centerX + innerRadius * cos(angle)
                        val y = centerY + innerRadius * sin(angle)
                        if (i == 0) moveTo(x, y) else lineTo(x, y)
                    }
                    close()
                }
                drawPath(
                    path = innerPath,
                    color = if (isEarned) badgeColor.copy(alpha = 0.3f) else Color.Gray.copy(alpha = 0.1f),
                    style = Fill
                )
            }

            // Tier texto
            Text(
                text = "T${certification.tier}",
                style = MaterialTheme.typography.labelLarge.copy(
                    color = Color.White,
                    fontWeight = FontWeight.Black,
                    fontSize = (size * 0.18f).sp
                )
            )
        }

        Spacer(modifier = Modifier.height(6.dp))

        // Nombre de la certificación
        Text(
            text = certification.displayName,
            style = MaterialTheme.typography.labelSmall.copy(
                fontWeight = if (isEarned) FontWeight.Bold else FontWeight.Normal,
                color = if (isEarned) colors.onBackground else colors.onBackground.copy(alpha = 0.5f),
                textAlign = TextAlign.Center
            ),
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )
    }
}

/**
 * Fila de mini-badges para mostrar en perfiles o resúmenes.
 */
@Composable
fun CertBadgeRow(
    certifications: List<CertificationType>,
    earnedTypes: List<CertificationType>,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        certifications.take(6).forEach { cert ->
            CertBadge(
                certification = cert,
                isEarned = cert in earnedTypes,
                size = 50f
            )
        }
    }
}
