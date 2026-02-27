import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/models/badge.dart';
import '../../core/models/child_profile.dart';
import '../../core/models/parental_settings.dart';
import '../../core/providers/app_providers.dart';
import '../../core/theme/app_theme.dart';
import '../widgets/badge_card.dart';
import '../widgets/glass_container.dart';
import '../widgets/island_background.dart';

/// Dashboard de Control Parental con bloqueo matemático
class ParentalDashboardScreen extends ConsumerStatefulWidget {
  const ParentalDashboardScreen({super.key});

  @override
  ConsumerState<ParentalDashboardScreen> createState() =>
      _ParentalDashboardScreenState();
}

class _ParentalDashboardScreenState
    extends ConsumerState<ParentalDashboardScreen> {
  bool _isAuthenticated = false;
  int _num1 = 0;
  int _num2 = 0;
  String _operation = '';
  final _answerController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _generateMathProblem();
  }

  void _generateMathProblem() {
    final random = Random();
    _num1 = random.nextInt(10) + 1;
    _num2 = random.nextInt(10) + 1;

    final operations = ['+', '-'];
    _operation = operations[random.nextInt(operations.length)];

    if (_operation == '-' && _num1 < _num2) {
      final temp = _num1;
      _num1 = _num2;
      _num2 = temp;
    }
  }

  int _getCorrectAnswer() {
    switch (_operation) {
      case '+':
        return _num1 + _num2;
      case '-':
        return _num1 - _num2;
      default:
        return 0;
    }
  }

  void _checkAnswer() {
    final answer = int.tryParse(_answerController.text);
    if (answer == _getCorrectAnswer()) {
      setState(() => _isAuthenticated = true);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Respuesta incorrecta. Intenta de nuevo.'),
          backgroundColor: IslaColors.error,
        ),
      );
      _answerController.clear();
      _generateMathProblem();
    }
  }

  @override
  void dispose() {
    _answerController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final profile = ref.watch(currentProfileProvider);
    final settings = ref.watch(parentalSettingsProvider);
    final size = MediaQuery.of(context).size;
    final isSmallScreen = size.width <= 360;

    return Scaffold(
      body: IslandBackground(
        child: SafeArea(
          child: !_isAuthenticated
              ? _buildAuthScreen(isSmallScreen)
              : _buildDashboard(profile, settings, isSmallScreen),
        ),
      ),
    );
  }

  Widget _buildAuthScreen(bool isSmallScreen) {
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              'assets/icons/app_icon.png',
              height: isSmallScreen ? 80 : 100,
            ),
            const SizedBox(height: 24),
            Text(
              'Acceso para Padres',
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    color: IslaColors.oceanDark,
                    fontWeight: FontWeight.w900,
                  ),
            ),
            const SizedBox(height: 32),
            GlassContainer(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  Text(
                    'Resuelve para entrar:',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          color: IslaColors.oceanDark,
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    '$_num1 $_operation $_num2 = ?',
                    style: Theme.of(context).textTheme.displayMedium?.copyWith(
                          color: IslaColors.oceanBlue,
                          fontWeight: FontWeight.w900,
                        ),
                  ),
                  const SizedBox(height: 24),
                  TextField(
                    controller: _answerController,
                    keyboardType: TextInputType.number,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: IslaColors.oceanDark,
                    ),
                    decoration: InputDecoration(
                      hintText: '?',
                      filled: true,
                      fillColor: Colors.white.withValues(alpha: 0.5),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(16),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _checkAnswer,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: IslaColors.oceanBlue,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                      child: const Text(
                        'VERIFICAR',
                        style: TextStyle(
                            fontWeight: FontWeight.w900, fontSize: 18),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text(
                'VOLVER',
                style: TextStyle(
                  color: IslaColors.oceanDark,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.2,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDashboard(ChildProfile? profile, ParentalSettings settings, bool isSmallScreen) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildDashboardHeader(isSmallScreen),
          const SizedBox(height: 24),
          _buildChildStats(profile, isSmallScreen),
          const SizedBox(height: 16),
          _buildTimeLimitCard(settings, isSmallScreen),
          const SizedBox(height: 16),
          _buildSoundSettingsCard(settings, isSmallScreen),
          const SizedBox(height: 16),
          _buildBadgesCard(profile, isSmallScreen),
          const SizedBox(height: 32),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton.icon(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(Icons.logout),
              label: const Text(
                'SALIR DEL PANEL',
                style: TextStyle(fontWeight: FontWeight.w900),
              ),
              style: OutlinedButton.styleFrom(
                side: const BorderSide(color: IslaColors.oceanBlue, width: 2),
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _buildDashboardHeader(bool isSmallScreen) {
    return GlassContainer(
      padding: const EdgeInsets.all(16),
      borderRadius: 20,
      child: Row(
        children: [
          Image.asset(
            'assets/icons/app_icon.png',
            height: 48,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Panel de Control',
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        color: IslaColors.oceanDark,
                        fontWeight: FontWeight.w900,
                      ),
                ),
                Text(
                  'Configuración para padres',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: IslaColors.oceanDark.withValues(alpha: 0.7),
                        fontWeight: FontWeight.w600,
                      ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildChildStats(ChildProfile? profile, bool isSmallScreen) {
    if (profile == null) return const SizedBox.shrink();

    return GlassContainer(
      borderRadius: 20,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Progreso de ${profile.name}',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  color: IslaColors.oceanDark,
                  fontWeight: FontWeight.w900,
                ),
          ),
          const SizedBox(height: 16),
          _buildStatRow(Icons.timer, 'Tiempo total', '${profile.totalPlayTimeMinutes} min'),
          const Divider(color: Colors.white24),
          _buildStatRow(Icons.emoji_events, 'Insignias', '${profile.earnedBadges.length}'),
          const Divider(color: Colors.white24),
          _buildStatRow(Icons.trending_up, 'Nivel actual', '${profile.currentLevel}'),
        ],
      ),
    );
  }

  Widget _buildStatRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Icon(icon, color: IslaColors.oceanBlue, size: 20),
          const SizedBox(width: 12),
          Text(
            label,
            style: const TextStyle(fontWeight: FontWeight.w600, color: IslaColors.oceanDark),
          ),
          const Spacer(),
          Text(
            value,
            style: const TextStyle(fontWeight: FontWeight.w900, color: IslaColors.oceanBlue),
          ),
        ],
      ),
    );
  }

  Widget _buildTimeLimitCard(ParentalSettings settings, bool isSmallScreen) {
    return GlassContainer(
      borderRadius: 20,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.av_timer, color: IslaColors.sunsetCoral),
              const SizedBox(width: 8),
              Text(
                'Límite Diario',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w900,
                      color: IslaColors.oceanDark,
                    ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Slider(
            value: settings.dailyTimeLimitMinutes.toDouble(),
            min: 15,
            max: 120,
            divisions: 7,
            activeColor: IslaColors.oceanBlue,
            inactiveColor: IslaColors.oceanBlue.withValues(alpha: 0.2),
            label: '${settings.dailyTimeLimitMinutes} min',
            onChanged: (value) {
              ref.read(parentalSettingsProvider.notifier).updateTimeLimit(value.toInt());
            },
          ),
          Center(
            child: Text(
              '${settings.dailyTimeLimitMinutes} minutos',
              style: const TextStyle(fontWeight: FontWeight.w900, color: IslaColors.oceanBlue),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSoundSettingsCard(ParentalSettings settings, bool isSmallScreen) {
    return GlassContainer(
      borderRadius: 20,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Sonido y Música',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w900,
                  color: IslaColors.oceanDark,
                ),
          ),
          const SizedBox(height: 8),
          _buildSwitchTile(
            'Efectos de sonido',
            settings.soundEnabled,
            (_) => ref.read(parentalSettingsProvider.notifier).toggleSound(),
          ),
          _buildSwitchTile(
            'Música de fondo',
            settings.musicEnabled,
            (_) => ref.read(parentalSettingsProvider.notifier).toggleMusic(),
          ),
        ],
      ),
    );
  }

  Widget _buildSwitchTile(String title, bool value, Function(bool) onChanged) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          title,
          style: const TextStyle(fontWeight: FontWeight.w600, color: IslaColors.oceanDark),
        ),
        Switch(
          value: value,
          onChanged: onChanged,
          activeThumbColor: IslaColors.oceanBlue,
        ),
      ],
    );
  }

  Widget _buildBadgesCard(ChildProfile? profile, bool isSmallScreen) {
    final earnedIds = profile?.earnedBadges ?? [];

    return GlassContainer(
      borderRadius: 20,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Catálogo de Insignias',
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w900,
                  color: IslaColors.oceanDark,
                ),
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: Wrap(
              spacing: 12,
              runSpacing: 12,
              alignment: WrapAlignment.center,
              children: IslaBadges.allBadges.map((badge) {
                return BadgeCard(
                  badge: badge,
                  isEarned: earnedIds.contains(badge.id),
                  size: isSmallScreen ? 48 : 56,
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }
}
