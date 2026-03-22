package com.liebeblack.isla_digital.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.unit.dp
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme

/**
 * Card adaptativa que cambia su estética según la fase del usuario.
 * - Sensorial: Bordes muy redondeados, sombras coloridas, fondo cálido
 * - Creativa: Bordes moderados, elevación media, estilo moderno
 * - Profesional: Bordes sutiles, mínima elevación, dark surface
 */
@Composable
fun AdaptiveCard(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    val colors = IslaAdaptiveTheme.colors
    val config = IslaAdaptiveTheme.typoConfig
    val shape = RoundedCornerShape(config.borderRadius.dp)

    Card(
        modifier = modifier
            .border(
                width = 1.dp,
                color = colors.cardBorder,
                shape = shape
            ),
        shape = shape,
        colors = CardDefaults.cardColors(
            containerColor = colors.surface
        ),
        elevation = CardDefaults.cardElevation(
            defaultElevation = config.elevation.dp
        )
    ) {
        Box(modifier = Modifier.padding(config.cardPadding.dp)) {
            content()
        }
    }
}

/**
 * Card Glass adaptativa — combina glassmorphism con el tema de fase.
 */
@Composable
fun AdaptiveGlassCard(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    val colors = IslaAdaptiveTheme.colors
    val config = IslaAdaptiveTheme.typoConfig
    val shape = RoundedCornerShape(config.borderRadius.dp)

    Box(
        modifier = modifier.clip(shape)
    ) {
        // Capa glass
        Box(
            modifier = Modifier
                .matchParentSize()
                .background(
                    brush = Brush.linearGradient(
                        colors = listOf(
                            colors.glassOverlay,
                            colors.glassOverlay.copy(alpha = colors.glassOverlay.alpha * 0.6f)
                        )
                    )
                )
                .border(
                    width = 1.dp,
                    brush = Brush.linearGradient(
                        colors = listOf(
                            colors.glassBorder,
                            colors.glassBorder.copy(alpha = colors.glassBorder.alpha * 0.3f)
                        )
                    ),
                    shape = shape
                )
        )
        // Contenido
        Box(modifier = Modifier.padding(config.cardPadding.dp)) {
            content()
        }
    }
}
