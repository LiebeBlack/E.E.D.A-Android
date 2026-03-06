import 'package:flutter/foundation.dart';

@immutable
class ParentalSettings {
  // 2. CONSTRUCTOR CONST (Movido arriba)
  const ParentalSettings({
    this.dailyTimeLimitMinutes = 30,
    this.soundEnabled = true,
    this.musicEnabled = true,
    this.notificationsEnabled = true,
    this.allowedContacts = const [],
    this.lastAccess,
  });

  // 3. FACTORY CONSTRUCTOR (Movido arriba)
  factory ParentalSettings.fromJson(Map<String, dynamic> json) {
    return ParentalSettings(
      dailyTimeLimitMinutes:
          (json['dailyTimeLimitMinutes'] as num?)?.toInt() ?? 30,
      soundEnabled: json['soundEnabled'] as bool? ?? true,
      musicEnabled: json['musicEnabled'] as bool? ?? true,
      notificationsEnabled: json['notificationsEnabled'] as bool? ?? true,
      allowedContacts:
          List<String>.from(json['allowedContacts'] as List? ?? []),
      lastAccess: json['lastAccess'] != null
          ? DateTime.tryParse(json['lastAccess'].toString())
          : null,
    );
  }
  // 1. Propiedades Finales
  final int dailyTimeLimitMinutes;
  final bool soundEnabled;
  final bool musicEnabled;
  final bool notificationsEnabled;
  final List<String> allowedContacts;
  final DateTime? lastAccess;

  // 4. MÉTODOS
  Map<String, dynamic> toJson() => {
        'dailyTimeLimitMinutes': dailyTimeLimitMinutes,
        'soundEnabled': soundEnabled,
        'musicEnabled': musicEnabled,
        'notificationsEnabled': notificationsEnabled,
        'allowedContacts': allowedContacts,
        'lastAccess': lastAccess?.toIso8601String(),
      };

  ParentalSettings copyWith({
    int? dailyTimeLimitMinutes,
    bool? soundEnabled,
    bool? musicEnabled,
    bool? notificationsEnabled,
    List<String>? allowedContacts,
    ValueGetter<DateTime?>? lastAccess,
  }) {
    return ParentalSettings(
      dailyTimeLimitMinutes:
          dailyTimeLimitMinutes ?? this.dailyTimeLimitMinutes,
      soundEnabled: soundEnabled ?? this.soundEnabled,
      musicEnabled: musicEnabled ?? this.musicEnabled,
      notificationsEnabled: notificationsEnabled ?? this.notificationsEnabled,
      allowedContacts:
          allowedContacts ?? List<String>.from(this.allowedContacts),
      lastAccess: lastAccess != null ? lastAccess() : this.lastAccess,
    );
  }

  @override
  String toString() =>
      'ParentalSettings(limit: $dailyTimeLimitMinutes min, music: $musicEnabled)';
}
