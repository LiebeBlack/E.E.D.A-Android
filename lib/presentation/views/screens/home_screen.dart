import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:isla_digital/core/theme/app_theme.dart';
import 'package:isla_digital/presentation/providers/app_providers.dart';
import 'package:isla_digital/presentation/widgets/big_button.dart';
import 'package:isla_digital/presentation/widgets/glass_container.dart';
import 'package:isla_digital/presentation/widgets/island_background.dart';
import 'package:isla_digital/presentation/widgets/safe_lottie.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final profileName = ref.watch(currentProfileProvider.select((p) => p?.name ?? 'Explorador'));
    final badgesCount = ref.watch(currentProfileProvider.select((p) => p?.earnedBadges.length ?? 0));
    
    final size = MediaQuery.sizeOf(context);
    final isSmallScreen = size.width <= 360;

    return Scaffold(
      extendBody: true, 
      body: IslandBackground(
        child: SafeArea(
          child: Stack(
            children: [
              CustomScrollView(
                physics: const BouncingScrollPhysics(),
                slivers: [
                  SliverToBoxAdapter(
                    child: _buildTopBar(context, profileName, badgesCount),
                  ),
                  
                  SliverFillRemaining(
                    hasScrollBody: false,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 24),
                      child: Column(
                        children: [
                          const SizedBox(height: 20),
                          _buildWelcomeHero(context),
                          const SizedBox(height: 40),
                          _buildActionsGrid(context, ref),
                          const Spacer(),
                          const SizedBox(height: 140), 
                        ],
                      ),
                    ),
                  ),
                ],
              ),
              
              _buildBottomCharacters(isSmallScreen),
              
              Positioned(
                top: 16,
                right: 16,
                child: _buildSettingsButton(context),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // --- COMPONENTES DE UI ---

  Widget _buildTopBar(BuildContext context, String name, int badges) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(24, 16, 80, 8),
      child: GlassContainer(
        child: Row(
          children: [
            Hero(
              tag: 'profile_avatar',
              child: Container(
                padding: const EdgeInsets.all(8),
                decoration: const BoxDecoration(
                  color: IslaColors.sunflower,
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.face_retouching_natural_rounded, color: Colors.white, size: 24),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // FIX: Uso de estilos definidos en IslaThemes (Paso 1)
                  Text('¡HOLA!', style: IslaThemes.labelStyle),
                  Text(
                    name.toUpperCase(),
                    style: IslaThemes.titleMediumStyle,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
            _buildBadgePill(badges),
          ],
        ),
      ),
    ).animate().fadeIn(duration: 600.ms).slideY(begin: -0.2, end: 0);
  }

  Widget _buildBadgePill(int count) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        // FIX: Cambiado .withOpacity por .withValues(alpha: ...)
        color: Colors.white.withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.stars_rounded, color: IslaColors.sunflower, size: 18),
          const SizedBox(width: 6),
          // FIX: Uso de estilo badgeCounterStyle
          Text('$count', style: IslaThemes.badgeCounterStyle),
        ],
      ),
    );
  }

  Widget _buildWelcomeHero(BuildContext context) {
    return Column(
      children: [
        const SafeLottie(
          path: 'assets/animations/ui/welcome_island.json',
          size: 200,
        ),
        const SizedBox(height: 16),
        // FIX: Uso de estilos display y subtitle
        Text('ISLA DIGITAL', style: IslaThemes.displayStyle),
        Text('¡TU AVENTURA COMIENZA AQUÍ!', style: IslaThemes.subtitleStyle),
      ],
    ).animate().scale(delay: 200.ms, curve: Curves.easeOutBack, duration: 800.ms);
  }

  Widget _buildActionsGrid(BuildContext context, WidgetRef ref) {
    return Column(
      children: [
        BigButton(
          icon: Icons.play_arrow_rounded,
          label: 'JUGAR',
          color: IslaColors.jungleGreen,
          onPressed: () => Navigator.pushNamed(context, '/levels'),
        ).animate().fadeIn(delay: 400.ms).slideX(begin: -0.1, end: 0),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: BigButton(
                icon: Icons.emoji_events_rounded,
                label: 'LOGROS',
                color: IslaColors.sunflower,
                onPressed: () => _showBadgesDialog(context, ref),
              ).animate().fadeIn(delay: 600.ms).slideX(begin: -0.1, end: 0),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: BigButton(
                icon: Icons.auto_awesome_mosaic_rounded,
                label: 'ÁLBUM',
                color: IslaColors.oceanBlue,
                onPressed: () => Navigator.pushNamed(context, '/showcase'),
              ).animate().fadeIn(delay: 600.ms).slideX(begin: 0.1, end: 0),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildBottomCharacters(bool isSmallScreen) {
    return Positioned(
      bottom: -10,
      left: 0,
      right: 0,
      child: IgnorePointer(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            const SafeLottie(
              path: 'assets/animations/characters/giraffe_hello.json',
            ),
            SafeLottie(
              path: 'assets/animations/characters/cat_wave.json',
              size: isSmallScreen ? 110 : 140,
            ),
          ],
        ),
      ),
    ).animate().slideY(begin: 0.5, end: 0, delay: 800.ms, curve: Curves.easeOut);
  }

  Widget _buildSettingsButton(BuildContext context) {
    return DecoratedBox(
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.3),
        shape: BoxShape.circle,
        border: Border.all(color: Colors.white.withValues(alpha: 0.5), width: 1.5),
      ),
      child: IconButton(
        icon: const Icon(Icons.settings_rounded, color: IslaColors.oceanDark),
        onPressed: () => _showSettingsMenu(context),
      ),
    );
  }

  // --- LÓGICA DE DIÁLOGOS ---

  void _showSettingsMenu(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(32)),
        title: const Text('ZONA DE PADRES', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.w900)),
        content: const Text('¿Deseas entrar a la configuración parental?', textAlign: TextAlign.center),
        actionsAlignment: MainAxisAlignment.center,
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('CANCELAR'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: IslaColors.oceanBlue, 
              foregroundColor: Colors.white,
              minimumSize: const Size(100, 45), // Tamaño adaptado para diálogo
            ),
            onPressed: () {
              Navigator.pop(context);
              Navigator.pushNamed(context, '/parental');
            },
            child: const Text('ENTRAR'),
          ),
        ],
      ),
    );
  }

  void _showBadgesDialog(BuildContext context, WidgetRef ref) {
    showGeneralDialog(
      context: context,
      barrierDismissible: true,
      barrierLabel: 'Badges',
      transitionDuration: const Duration(milliseconds: 400),
      pageBuilder: (context, anim1, anim2) => Center(
        child: Material(
          color: Colors.transparent,
          child: Container(
            margin: const EdgeInsets.all(24),
            child: GlassContainer(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('TUS TROFEOS', 
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: IslaColors.oceanDark)),
                  const SizedBox(height: 20),
                  ConstrainedBox(
                    constraints: BoxConstraints(maxHeight: MediaQuery.sizeOf(context).height * 0.4),
                    child: GridView.builder(
                      shrinkWrap: true,
                      itemCount: 12, 
                      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 3,
                        mainAxisSpacing: 12,
                        crossAxisSpacing: 12,
                      ),
                      itemBuilder: (context, index) {
                        return DecoratedBox(
                          decoration: BoxDecoration(
                            color: Colors.white.withValues(alpha: 0.24),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Icon(Icons.lock_outline, color: IslaColors.slate),
                        );
                      },
                    ),
                  ),
                  const SizedBox(height: 24),
                  BigButton(
                    icon: Icons.check,
                    label: '¡LISTO!',
                    color: IslaColors.jungleGreen,
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
            ),
          ),
        ).animate().scale(curve: Curves.elasticOut, duration: 600.ms),
      ),
    );
  }
}