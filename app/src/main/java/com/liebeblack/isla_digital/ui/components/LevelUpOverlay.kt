package com.liebeblack.isla_digital.ui.components

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AutoAwesome
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.liebeblack.isla_digital.ui.theme.IslaAdaptiveTheme
import kotlinx.coroutines.delay
import android.view.animation.Interpolator
import android.view.animation.OvershootInterpolator

/**
 * Overlay minimalista y premium para celebrar niveles alcanzados.
 */
@Composable
fun LevelUpOverlay(
    level: Int,
    isVisible: Boolean,
    onDismiss: () -> Unit
) {
    if (!isVisible) return

    val colors = IslaAdaptiveTheme.colors
    var showContent by remember { mutableStateOf(false) }

    LaunchedEffect(isVisible) {
        if (isVisible) {
            delay(200)
            showContent = true
            delay(2500)
            onDismiss()
        }
    }

    Box(
        modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.5f)),
        contentAlignment = Alignment.Center
    ) {
        AnimatedVisibility(
            visible = showContent,
            enter = fadeIn() + scaleIn(tween(600, easing = OvershootInterpolator(2f).asEasing())),
            exit = fadeOut()
        ) {
            Surface(
                modifier = Modifier.padding(32.dp),
                shape = CircleShape,
                color = colors.surface,
                tonalElevation = 8.dp,
                shadowElevation = 12.dp
            ) {
                Column(
                    modifier = Modifier.padding(32.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(Icons.Rounded.AutoAwesome, null, Modifier.size(48.dp), tint = colors.secondary)
                    Spacer(Modifier.height(8.dp))
                    Text("¡NUEVO NIVEL!", style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Black, color = colors.secondary, letterSpacing = 2.sp))
                    Text("$level", style = MaterialTheme.typography.displayLarge.copy(fontWeight = FontWeight.Black, color = colors.primary))
                    Text("Sigue así, explorador", style = MaterialTheme.typography.bodySmall.copy(color = colors.onSurface.copy(alpha = 0.6f)))
                }
            }
        }
    }
}

private fun Interpolator.asEasing() = Easing { x -> getInterpolation(x) }
