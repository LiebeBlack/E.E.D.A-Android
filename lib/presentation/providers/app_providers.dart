import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:isla_digital/core/services/services.dart';
import 'package:isla_digital/domain/models/models.dart';

// --- PROFILE PROVIDER ---

class ProfileNotifier extends StateNotifier<ChildProfile?> {
  ProfileNotifier() : super(null) {
    _loadSavedProfile();
  }

  void _loadSavedProfile() {
    state = LocalStorageService.loadProfile();
  }

  // --- MÉTODOS DE ACCIÓN ---

  Future<void> createProfile(String name, int age, {String avatar = 'default'}) async {
    final profile = ChildProfile(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: name,
      age: age,
      avatar: avatar,
    );
    await _updateAndSave(profile);
  }

  /// FIX: Agregado el método que los niveles están reclamando
  Future<void> unlockLevel(int levelNumber) async {
    if (state == null) return;
    
    // Solo actualizamos si el nivel a desbloquear es mayor al actual
    if (levelNumber > state!.currentLevel) {
      final updatedProfile = state!.copyWith(currentLevel: levelNumber);
      await _updateAndSave(updatedProfile);
      debugPrint('🎉 ¡Nivel $levelNumber desbloqueado!');
    }
  }

  Future<void> updateProfile({String? name, int? age, String? avatar}) async {
    if (state == null) return;
    await _updateAndSave(state!.copyWith(
      name: name,
      age: age,
      avatar: avatar,
    ));
  }

  Future<void> addProgress(String levelId, int points) async {
    if (state == null) return;
    final newProgress = Map<String, int>.from(state!.levelProgress);
    newProgress[levelId] = (newProgress[levelId] ?? 0) + points;

    await _updateAndSave(state!.copyWith(levelProgress: newProgress));
    await LocalStorageService.saveLevelProgress(levelId, newProgress[levelId]!);
  }

  Future<void> addBadge(String badgeId) async {
    if (state == null || state!.earnedBadges.contains(badgeId)) return;
    
    final newBadges = [...state!.earnedBadges, badgeId];
    await _updateAndSave(state!.copyWith(earnedBadges: newBadges));
    await LocalStorageService.addBadge(badgeId);
  }

  Future<void> _updateAndSave(ChildProfile profile) async {
    state = profile;
    await LocalStorageService.saveProfile(profile);
  }

  Future<void> clear() async {
    state = null;
    await LocalStorageService.deleteProfile();
  }
}

final currentProfileProvider = StateNotifierProvider<ProfileNotifier, ChildProfile?>((ref) {
  return ProfileNotifier();
});

// --- PARENTAL SETTINGS PROVIDER ---

class ParentalSettingsNotifier extends StateNotifier<ParentalSettings> {
  ParentalSettingsNotifier() : super(LocalStorageService.loadParentalSettings());

  Future<void> _update(ParentalSettings updated) async {
    state = updated;
    await LocalStorageService.saveParentalSettings(updated);
  }

  Future<void> updateTimeLimit(int minutes) => _update(state.copyWith(dailyTimeLimitMinutes: minutes));
  Future<void> toggleSound() => _update(state.copyWith(soundEnabled: !state.soundEnabled));
  Future<void> toggleMusic() => _update(state.copyWith(musicEnabled: !state.musicEnabled));
  Future<void> updateContacts(List<String> contacts) => _update(state.copyWith(allowedContacts: contacts));
}

final parentalSettingsProvider = StateNotifierProvider<ParentalSettingsNotifier, ParentalSettings>((ref) {
  return ParentalSettingsNotifier();
});

// --- APP UI STATE PROVIDER ---

@immutable
class AppState {

  // 2. CONSTRUCTOR (Movido aquí para corregir sort_constructors_first)
  const AppState({
    this.isLoading = false,
    this.currentRoute,
    this.showCelebration = false,
  });
  // 1. Propiedades
  final bool isLoading;
  final String? currentRoute;
  final bool showCelebration;

  // 3. Métodos
  AppState copyWith({bool? isLoading, String? currentRoute, bool? showCelebration}) {
    return AppState(
      isLoading: isLoading ?? this.isLoading,
      currentRoute: currentRoute ?? this.currentRoute,
      showCelebration: showCelebration ?? this.showCelebration,
    );
  }
}

class AppStateNotifier extends StateNotifier<AppState> {
  AppStateNotifier() : super(const AppState());

  void setLoading(bool loading) => state = state.copyWith(isLoading: loading);
  
  void triggerCelebration() {
    state = state.copyWith(showCelebration: true);
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) state = state.copyWith(showCelebration: false);
    });
  }
}

final appStateProvider = StateNotifierProvider<AppStateNotifier, AppState>((ref) => AppStateNotifier());

// --- LEVEL PROGRESS PROVIDER ---

final levelProgressProvider = StateProvider.family<int, String>((ref, levelId) {
  final profile = ref.watch(currentProfileProvider);
  return profile?.levelProgress[levelId] ?? 0;
});