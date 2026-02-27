import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/providers/app_providers.dart';
import '../../core/theme/app_theme.dart';
import '../../core/utils/color_utils.dart';
import '../levels/level1/level1_screen.dart';
import '../levels/level2/level2_screen.dart';
import '../levels/level3/level3_screen.dart';
import '../levels/level4/level4_screen.dart';
import '../levels/level5/level5_screen.dart';
import '../widgets/glass_container.dart';
import '../widgets/island_background.dart';
import '../widgets/progress_widgets.dart';

class LevelSelectScreen extends ConsumerWidget {
  const LevelSelectScreen({super.key});

  final List<Map<String, dynamic>> levels = const [
    {
      'id': 'level_1',
      'title': 'Mi Primer Encuentro',
      'subtitle': 'Aprende a usar tu teléfono',
      'icon': Icons.touch_app,
      'color': IslaColors.oceanBlue,
      'unlocked': true,
    },
    {
      'id': 'level_2',
      'title': 'Conectados',
      'subtitle': 'Llamadas y mensajes seguros',
      'icon': Icons.phone_in_talk,
      'color': IslaColors.palmGreen,
      'unlocked': false,
    },
    {
      'id': 'level_3',
      'title': 'Explorador Seguro',
      'subtitle': 'Detective de Internet',
      'icon': Icons.search,
      'color': IslaColors.sunsetPurple,
      'unlocked': false,
    },
    {
      'id': 'level_4',
      'title': 'Super Tareas',
      'subtitle': 'Calculadora y cámara',
      'icon': Icons.calculate,
      'color': IslaColors.sunsetCoral,
      'unlocked': false,
    },
    {
      'id': 'level_5',
      'title': 'Pequeño Artista',
      'subtitle': 'Dibuja y crea música',
      'icon': Icons.palette,
      'color': IslaColors.sunsetPink,
      'unlocked': false,
    },
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final profile = ref.watch(currentProfileProvider);
    final currentLevel = profile?.currentLevel ?? 1;
    final size = MediaQuery.of(context).size;
    final isSmallScreen = size.width <= 360;

    return Scaffold(
      body: IslandBackground(
        child: SafeArea(
          child: Column(
            children: [
              _buildHeader(context, isSmallScreen),
              const SizedBox(height: 8),
              Expanded(
                child: Padding(
                  padding: EdgeInsets.symmetric(
                    horizontal: isSmallScreen ? 12 : 16,
                  ),
                  child: GlassContainer(
                    padding: EdgeInsets.symmetric(
                      vertical: 16,
                      horizontal: isSmallScreen ? 8 : 12,
                    ),
                    child: ListView.builder(
                      physics: const BouncingScrollPhysics(),
                      itemCount: levels.length,
                      itemBuilder: (context, index) {
                        final level = levels[index];
                        final isUnlocked = index < currentLevel;
                        final isCurrent = index == currentLevel - 1;

                        return _buildLevelCard(
                          context,
                          level,
                          isUnlocked,
                          isCurrent,
                          profile?.levelProgress[level['id']] ?? 0,
                          isSmallScreen,
                        );
                      },
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context, bool isSmallScreen) {
    return Padding(
      padding: EdgeInsets.all(isSmallScreen ? 12 : 16),
      child: Row(
        children: [
          DecoratedBox(
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.3),
              shape: BoxShape.circle,
            ),
            child: IconButton(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(Icons.arrow_back, size: 24),
              color: IslaColors.oceanDark,
            ),
          ),
          const SizedBox(width: 12),
          Text(
            'Elige un Nivel',
            style: (isSmallScreen
                    ? Theme.of(context).textTheme.headlineSmall
                    : Theme.of(context).textTheme.headlineMedium)
                ?.copyWith(
              color: IslaColors.oceanDark,
              fontWeight: FontWeight.w900,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLevelCard(
    BuildContext context,
    Map<String, dynamic> level,
    bool isUnlocked,
    bool isCurrent,
    int progress,
    bool isSmallScreen,
  ) {
    final color = level['color'] as Color;

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      child: Opacity(
        opacity: isUnlocked ? 1.0 : 0.6,
        child: InkWell(
          onTap: isUnlocked
              ? () => _navigateToLevel(context, level['id'] as String)
              : null,
          borderRadius: BorderRadius.circular(20),
          child: Container(
            padding: EdgeInsets.all(isSmallScreen ? 12 : 16),
            decoration: BoxDecoration(
              color: isCurrent
                  ? color.withValues(alpha: 0.15)
                  : Colors.white.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(
                color: isCurrent ? color : Colors.white.withValues(alpha: 0.2),
                width: isCurrent ? 2.5 : 1.5,
              ),
            ),
            child: Row(
              children: [
                Container(
                  width: isSmallScreen ? 50 : 64,
                  height: isSmallScreen ? 50 : 64,
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [color, ColorUtils.darken(color, 0.2)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [
                      BoxShadow(
                        color: color.withValues(alpha: 0.3),
                        blurRadius: 8,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Icon(
                    level['icon'] as IconData,
                    size: isSmallScreen ? 28 : 36,
                    color: IslaColors.white,
                  ),
                ),
                SizedBox(width: isSmallScreen ? 12 : 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        level['title'] as String,
                        style: (isSmallScreen
                                ? Theme.of(context).textTheme.titleMedium
                                : Theme.of(context).textTheme.titleLarge)
                            ?.copyWith(
                          fontWeight: FontWeight.w900,
                          color: IslaColors.oceanDark,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        level['subtitle'] as String,
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                              color: IslaColors.oceanDark.withValues(alpha: 0.8),
                              fontWeight: FontWeight.w600,
                            ),
                      ),
                      if (isUnlocked) ...[
                        const SizedBox(height: 8),
                        IslandProgressBar(
                          progress: progress,
                          height: isSmallScreen ? 8 : 10,
                          fillColor: color,
                          showPercentage: false,
                        ),
                      ],
                    ],
                  ),
                ),
                if (!isUnlocked)
                  const Icon(
                    Icons.lock,
                    color: IslaColors.oceanDark,
                    size: 24,
                  )
                else if (progress >= 100)
                  const Icon(
                    Icons.check_circle,
                    color: IslaColors.palmGreen,
                    size: 28,
                  )
                else
                  Icon(
                    Icons.play_circle_fill,
                    color: color,
                    size: 28,
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _navigateToLevel(BuildContext context, String levelId) {
    switch (levelId) {
      case 'level_1':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const Level1Screen()),
        );
        break;
      case 'level_2':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const Level2Screen()),
        );
        break;
      case 'level_3':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const Level3Screen()),
        );
        break;
      case 'level_4':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const Level4Screen()),
        );
        break;
      case 'level_5':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const Level5Screen()),
        );
        break;
      default:
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Nivel no disponible')),
        );
    }
  }
}
