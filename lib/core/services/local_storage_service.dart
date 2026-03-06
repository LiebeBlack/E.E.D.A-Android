import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:isla_digital/domain/models/models.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Servicio de persistencia local optimizado con tipado fuerte
class LocalStorageService {
  static const String _profileKey = 'child_profile';
  static const String _settingsKey = 'parental_settings';
  static const String _badgesKey = 'earned_badges';
  static const String _playTimeKey = 'total_play_time';
  static const String _lastSessionKey = 'last_session';
  static const String _levelProgressPrefix = 'progress_';

  static SharedPreferences? _prefs;

  static Future<void> initialize() async {
    if (_prefs != null) return;
    try {
      _prefs = await SharedPreferences.getInstance();
      debugPrint('💾 LocalStorageService: Inicializado correctamente');
    } catch (e) {
      debugPrint('❌ Error al inicializar SharedPreferences: $e');
      rethrow;
    }
  }

  static SharedPreferences get _p {
    if (_prefs == null) {
      throw Exception(
          'LocalStorageService no inicializado. Llama a initialize() primero.');
    }
    return _prefs!;
  }

  // --- PERFIL ---

  static Future<bool> saveProfile(ChildProfile profile) async {
    return await _p.setString(_profileKey, jsonEncode(profile.toJson()));
  }

  static ChildProfile? loadProfile() {
    final jsonString = _p.getString(_profileKey);
    if (jsonString == null || jsonString.isEmpty) return null;

    try {
      // FIX: Cast explícito de dynamic a Map<String, dynamic>
      final dynamic decoded = jsonDecode(jsonString);
      final Map<String, dynamic> map =
          Map<String, dynamic>.from(decoded as Map);
      return ChildProfile.fromJson(map);
    } catch (e) {
      debugPrint('❌ Error al deserializar perfil: $e');
      return null;
    }
  }

  static Future<bool> deleteProfile() => _p.remove(_profileKey);

  // --- CONFIGURACIÓN PARENTAL ---

  static Future<bool> saveParentalSettings(ParentalSettings settings) async {
    return await _p.setString(_settingsKey, jsonEncode(settings.toJson()));
  }

  static ParentalSettings loadParentalSettings() {
    final jsonString = _p.getString(_settingsKey);
    if (jsonString == null) return const ParentalSettings();

    try {
      // FIX: Cast explícito para el constructor fromJson
      final dynamic decoded = jsonDecode(jsonString);
      final Map<String, dynamic> map =
          Map<String, dynamic>.from(decoded as Map);
      return ParentalSettings.fromJson(map);
    } catch (e) {
      return const ParentalSettings();
    }
  }

  // --- TIEMPO DE JUEGO Y SESIÓN ---

  static Future<bool> savePlayTime(int minutes) =>
      _p.setInt(_playTimeKey, minutes);
  static int loadPlayTime() => _p.getInt(_playTimeKey) ?? 0;

  static Future<int> addPlayTime(int minutes) async {
    final current = loadPlayTime();
    final updated = current + minutes;
    await savePlayTime(updated);
    return updated;
  }

  static Future<bool> saveLastSession() {
    return _p.setString(_lastSessionKey, DateTime.now().toIso8601String());
  }

  static DateTime? loadLastSession() {
    final dateString = _p.getString(_lastSessionKey);
    return (dateString != null) ? DateTime.tryParse(dateString) : null;
  }

  static bool isNewDay() {
    final lastSession = loadLastSession();
    if (lastSession == null) return true;

    final now = DateTime.now();
    return lastSession.year != now.year ||
        lastSession.month != now.month ||
        lastSession.day != now.day;
  }

  // --- PROGRESO E INSIGNIAS ---

  static Future<bool> saveLevelProgress(String levelId, int progress) {
    return _p.setInt('$_levelProgressPrefix$levelId', progress);
  }

  static int loadLevelProgress(String levelId) {
    return _p.getInt('$_levelProgressPrefix$levelId') ?? 0;
  }

  static Future<bool> saveEarnedBadges(List<String> badges) {
    return _p.setStringList(_badgesKey, badges);
  }

  static List<String> loadEarnedBadges() => _p.getStringList(_badgesKey) ?? [];

  static Future<List<String>> addBadge(String badgeId) async {
    final badges = loadEarnedBadges();
    if (!badges.contains(badgeId)) {
      final updatedBadges = List<String>.from(badges)..add(badgeId);
      await saveEarnedBadges(updatedBadges);
      return updatedBadges;
    }
    return badges;
  }

  // --- UTILIDADES ---

  static Future<bool> clearAll() => _p.clear();

  static Map<String, dynamic> getStatsForParents() {
    return {
      'profileName': loadProfile()?.name ?? 'Sin nombre',
      'totalPlayTimeMinutes': loadPlayTime(),
      'badgesCount': loadEarnedBadges().length,
      'lastActive': loadLastSession()?.toIso8601String() ?? 'Nunca',
      'isNewDay': isNewDay(),
    };
  }
}
