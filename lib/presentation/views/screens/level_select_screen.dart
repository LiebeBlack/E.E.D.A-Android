import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:isla_digital/core/theme/app_theme.dart';
import 'package:isla_digital/presentation/providers/app_providers.dart';

// FIX: Rutas corregidas según tu estructura de carpetas real
import 'package:isla_digital/presentation/views/levels/level1/level1_screen.dart';
import 'package:isla_digital/presentation/views/levels/level2/level2_screen.dart';

import 'package:isla_digital/presentation/widgets/glass_container.dart';
import 'package:isla_digital/presentation/widgets/island_background.dart';
import 'package:isla_digital/presentation/widgets/progress_widgets.dart';

class LevelSelectScreen extends ConsumerWidget {
  // FIX: Constructor al inicio para cumplir con el linter
  const LevelSelectScreen({super.key});

  static const List<Map<String, dynamic>> levelsData = [
    {
      'id': 'level_1',
      'title': 'BIENVENIDA',
      'subtitle': 'HOLA TELÉFONO',
      'icon': Icons.smartphone_rounded,
      'color': IslaColors.oceanBlue,
    },
    {
      'id': 'level_2',
      'title': 'CONECTADOS',
      'subtitle': 'AMIGOS SEGUROS',
      'icon': Icons.forum_rounded,
      'color': IslaColors.jungleGreen,
    },
    {
      'id': 'level_3',
      'title': 'DETECTIVE',
      'subtitle': 'INTERNET GENIAL',
      'icon': Icons.search_rounded,
      'color': IslaColors.sunflower,
    },
    {
      'id': 'level_4',
      'title': 'MAESTRO',
      'subtitle': 'SÚPER TAREAS',
      'icon': Icons.auto_stories_rounded,
      'color': IslaColors.coralReef,
    },
    {
      'id': 'level_5',
      'title': 'ARTISTA',
      'subtitle': 'PINTA Y TOCA',
      'icon': Icons.palette_rounded,
      'color': IslaColors.sunsetPink,
    },
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // FIX: Usamos currentLevel (entero) para comparar con el índice
    final currentLevelUnlocked = ref.watch(currentProfileProvider.select((p) => p?.currentLevel ?? 1));
    final levelProgressMap = ref.watch(currentProfileProvider.select((p) => p?.levelProgress ?? {}));

    return Scaffold(
      extendBodyBehindAppBar: true,
      body: IslandBackground(
        child: SafeArea(
          bottom: false,
          child: Column(
            children: [
              _buildHeader(context),
              Expanded(
                child: ListView.builder(
                  padding: const EdgeInsets.fromLTRB(24, 8, 24, 100),
                  physics: const BouncingScrollPhysics(),
                  itemCount: levelsData.length,
                  itemBuilder: (context, index) {
                    final level = levelsData[index];
                    final levelId = level['id'] as String;
                    final isUnlocked = (index + 1) <= currentLevelUnlocked;
                    final progress = levelProgressMap[levelId] ?? 0;

                    return _LevelListItem(
                      index: index,
                      level: level,
                      isUnlocked: isUnlocked,
                      progress: progress,
                      onTap: () => _navigateToLevel(context, levelId),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          IconButton(
            icon: const Icon(Icons.arrow_back_ios_new_rounded, color: IslaColors.oceanDark),
            onPressed: () => Navigator.pop(context),
          ),
          const Expanded(
            child: Text(
              'MI MAPA',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 28,
                // FIX: w900 en lugar de black
                fontWeight: FontWeight.w900,
                color: IslaColors.oceanDark,
                letterSpacing: 1.5,
              ),
            ),
          ),
          const SizedBox(width: 48),
        ],
      ),
    ).animate().fadeIn().slideY(begin: -0.2, end: 0);
  }

  void _navigateToLevel(BuildContext context, String levelId) {
    Widget screen;
    switch (levelId) {
      case 'level_1': screen = const Level1Screen(); break;
      case 'level_2': screen = const Level2Screen(); break;
      default: return;
    }

    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => screen),
    );
  }
}

class _LevelListItem extends StatelessWidget {
  // FIX: Constructor al inicio
  const _LevelListItem({
    required this.index,
    required this.level,
    required this.isUnlocked,
    required this.progress,
    required this.onTap,
  });

  final int index;
  final Map<String, dynamic> level;
  final bool isUnlocked;
  final int progress;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final color = level['color'] as Color;
    final bool isCompleted = progress >= 100;

    return Padding(
      padding: const EdgeInsets.only(bottom: 20),
      child: GestureDetector(
        onTap: isUnlocked ? onTap : () {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: const Text('¡Sigue jugando para desbloquear este nivel!'),
              backgroundColor: IslaColors.oceanDark,
              behavior: SnackBarBehavior.floating,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
          );
        },
        child: GlassContainer(
          padding: const EdgeInsets.all(16),
          child: Opacity(
            opacity: isUnlocked ? 1.0 : 0.5,
            child: Row(
              children: [
                _LevelIcon(
                  icon: level['icon'] as IconData,
                  color: color,
                  isUnlocked: isUnlocked,
                ),
                const SizedBox(width: 20),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        level['title'] as String,
                        style: TextStyle(
                          fontSize: 18,
                          // FIX: w900 en lugar de black
                          fontWeight: FontWeight.w900,
                          color: isUnlocked ? IslaColors.oceanDark : Colors.grey[700],
                        ),
                      ),
                      Text(
                        level['subtitle'] as String,
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.bold,
                          color: IslaColors.oceanDark.withValues(alpha: 0.6),
                        ),
                      ),
                      if (isUnlocked && progress > 0 && !isCompleted) ...[
                        const SizedBox(height: 12),
                        IslandProgressBar(
                          progress: progress,
                          height: 8,
                          fillColor: color,
                        ),
                      ],
                    ],
                  ),
                ),
                _buildStatusIndicator(isCompleted, color),
              ],
            ),
          ),
        ),
      ),
    ).animate().fadeIn(delay: (index * 80).ms).slideX(begin: 0.2, end: 0);
  }

  Widget _buildStatusIndicator(bool isCompleted, Color color) {
    if (!isUnlocked) return const Icon(Icons.lock_outline_rounded, color: Colors.grey);
    
    return isCompleted
        ? const Icon(Icons.check_circle_rounded, color: IslaColors.jungleGreen, size: 36)
            .animate(onPlay: (c) => c.repeat())
            .shimmer(duration: 2.seconds, color: Colors.white)
        : Icon(Icons.play_circle_filled_rounded, color: color, size: 36);
  }
}

class _LevelIcon extends StatelessWidget {
  // FIX: Constructor al inicio
  const _LevelIcon({required this.icon, required this.color, required this.isUnlocked});

  final IconData icon;
  final Color color;
  final bool isUnlocked;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 60,
      height: 60,
      decoration: BoxDecoration(
        color: isUnlocked ? color : Colors.grey[300],
        borderRadius: BorderRadius.circular(18),
        boxShadow: isUnlocked ? [
          BoxShadow(color: color.withValues(alpha: 0.4), blurRadius: 8, offset: const Offset(0, 4))
        ] : null,
      ),
      child: Icon(
        isUnlocked ? icon : Icons.lock_rounded,
        color: isUnlocked ? Colors.white : Colors.grey[600],
        size: 30,
      ),
    );
  }
}