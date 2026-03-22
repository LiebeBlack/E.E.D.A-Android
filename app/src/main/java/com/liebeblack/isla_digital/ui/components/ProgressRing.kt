package com.liebeblack.isla_digital.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme

/**
 * Anillo de progreso circular animado con porcentaje.
 * Se adapta a los colores de la fase actual.
 */
@Composable
fun ProgressRing(
    progress: Float, // 0f a 1f
    modifier: Modifier = Modifier,
    size: Dp = 120.dp,
    strokeWidth: Dp = 10.dp,
    showPercentage: Boolean = true,
    trackColor: Color = IslaAdaptiveTheme.colors.progressTrack,
    fillColor: Color = IslaAdaptiveTheme.colors.progressFill,
    label: String? = null
) {
    val animatedProgress by animateFloatAsState(
        targetValue = progress.coerceIn(0f, 1f),
        animationSpec = tween(durationMillis = 1000, easing = FastOutSlowInEasing),
        label = "progressAnimation"
    )

    Box(
        modifier = modifier.size(size),
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.size(size)) {
            val canvasSize = this.size.minDimension
            val stroke = strokeWidth.toPx()
            val arcSize = Size(canvasSize - stroke, canvasSize - stroke)
            val topLeft = Offset(stroke / 2f, stroke / 2f)

            // Pista del fondo
            drawArc(
                color = trackColor,
                startAngle = -90f,
                sweepAngle = 360f,
                useCenter = false,
                topLeft = topLeft,
                size = arcSize,
                style = Stroke(width = stroke, cap = StrokeCap.Round)
            )

            // Arco de progreso
            drawArc(
                color = fillColor,
                startAngle = -90f,
                sweepAngle = 360f * animatedProgress,
                useCenter = false,
                topLeft = topLeft,
                size = arcSize,
                style = Stroke(width = stroke, cap = StrokeCap.Round)
            )
        }

        // Texto central
        if (showPercentage) {
            Text(
                text = "${(animatedProgress * 100).toInt()}%",
                style = MaterialTheme.typography.titleMedium.copy(
                    fontWeight = FontWeight.Bold,
                    color = IslaAdaptiveTheme.colors.onBackground
                )
            )
        }

        if (label != null && !showPercentage) {
            Text(
                text = label,
                style = MaterialTheme.typography.labelSmall.copy(
                    color = IslaAdaptiveTheme.colors.onBackground
                )
            )
        }
    }
}

/**
 * Versión mini del anillo de progreso para uso en listas o cards.
 */
@Composable
fun MiniProgressRing(
    progress: Float,
    modifier: Modifier = Modifier,
    size: Dp = 40.dp,
    strokeWidth: Dp = 4.dp
) {
    ProgressRing(
        progress = progress,
        modifier = modifier,
        size = size,
        strokeWidth = strokeWidth,
        showPercentage = false
    )
}
