import 'package:flutter/foundation.dart';

@immutable
class ChildProfile {

  // 2. CONSTRUCTOR PRINCIPAL (Movido arriba para cumplir con las reglas del linter)
  ChildProfile({
    required this.id,
    required this.name,
    required this.age,
    this.avatar = 'default',
    DateTime? createdAt,
    this.totalPlayTimeMinutes = 0,
    this.currentLevel = 1,
    Map<String, int>? levelProgress,
    List<String>? earnedBadges,
  })  : createdAt = createdAt ?? DateTime.now(),
        levelProgress = levelProgress ?? const {},
        earnedBadges = earnedBadges ?? const [];

  // 3. FACTORY CONSTRUCTOR (También debe ir antes de los métodos normales)
  factory ChildProfile.fromJson(Map<String, dynamic> json) {
    return ChildProfile(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? 'Explorador',
      age: (json['age'] as num?)?.toInt() ?? 0,
      avatar: json['avatar']?.toString() ?? 'default',
      createdAt: DateTime.tryParse(json['createdAt']?.toString() ?? '') ?? DateTime.now(),
      totalPlayTimeMinutes: (json['totalPlayTimeMinutes'] as num?)?.toInt() ?? 0,
      currentLevel: (json['currentLevel'] as num?)?.toInt() ?? 1,
      levelProgress: Map<String, int>.from(json['levelProgress'] as Map? ?? {}),
      earnedBadges: List<String>.from(json['earnedBadges'] as List? ?? []),
    );
  }
  // 1. Variables de instancia (Propiedades finales)
  final String id;
  final String name;
  final int age;
  final String avatar;
  final DateTime createdAt;
  final int totalPlayTimeMinutes;
  final int currentLevel;
  final Map<String, int> levelProgress;
  final List<String> earnedBadges;

  // 4. MÉTODOS (toJson, copyWith, etc.)
  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'age': age,
        'avatar': avatar,
        'createdAt': createdAt.toIso8601String(),
        'totalPlayTimeMinutes': totalPlayTimeMinutes,
        'currentLevel': currentLevel,
        'levelProgress': levelProgress,
        'earnedBadges': earnedBadges,
      };

  ChildProfile copyWith({
    String? name,
    int? age,
    String? avatar,
    int? totalPlayTimeMinutes,
    int? currentLevel,
    Map<String, int>? levelProgress,
    List<String>? earnedBadges,
  }) {
    return ChildProfile(
      id: id, 
      name: name ?? this.name,
      age: age ?? this.age,
      avatar: avatar ?? this.avatar,
      createdAt: createdAt,
      totalPlayTimeMinutes: totalPlayTimeMinutes ?? this.totalPlayTimeMinutes,
      currentLevel: currentLevel ?? this.currentLevel,
      levelProgress: levelProgress ?? Map<String, int>.from(this.levelProgress),
      earnedBadges: earnedBadges ?? List<String>.from(this.earnedBadges),
    );
  }

  @override
  String toString() => 'ChildProfile(name: $name, level: $currentLevel, badges: ${earnedBadges.length})';
}