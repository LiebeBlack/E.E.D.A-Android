import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:isla_digital/core/theme/app_theme.dart';
import 'package:lottie/lottie.dart';

/// Un widget de animación Lottie que maneja fallos de carga
/// transformándolos en un ícono con efecto de "respiración".
class SafeLottie extends StatelessWidget {
  const SafeLottie({
    super.key,
    required this.path,
    this.backupIcon = Icons.extension_rounded,
    this.size = 150,
    this.repeat = true,
    this.fit = BoxFit.contain,
  });

  final String path;
  final IconData backupIcon;
  final double size;
  final bool repeat;
  final BoxFit fit;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: size,
      height: size,
      child: Lottie.asset(
        path,
        fit: fit,
        repeat: repeat,
        frameRate: FrameRate.composition, 
        errorBuilder: (context, error, stackTrace) {
          return _InternalBounceFallback(
            icon: backupIcon,
            size: size,
          );
        },
      ),
    );
  }
}

/// Widget privado para el efecto de rebote infinito en caso de error
class _InternalBounceFallback extends StatelessWidget {
  const _InternalBounceFallback({
    required this.icon, 
    required this.size,
  });

  final IconData icon;
  final double size;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Icon(
        icon,
        size: size * 0.6,
        color: IslaColors.oceanBlue.withValues(alpha: 0.5),
      )
      .animate(onPlay: (controller) => controller.repeat(reverse: true))
      .scale(
        begin: const Offset(0.8, 0.8),
        end: const Offset(1.1, 1.1),
        duration: 1000.ms,
        curve: Curves.easeInOutBack,
      )
      .fadeIn(duration: 500.ms),
    );
  }
}