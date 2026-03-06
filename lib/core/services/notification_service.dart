import 'dart:async';
import 'package:flutter/foundation.dart';

/// Un servicio simulado (Mock) que sienta las bases para notificaciones Push / Locales.
/// Prepara la arquitectura para una fácil integración futura (ej. flutter_local_notifications).
class NotificationService {
  factory NotificationService() => _instance;
  NotificationService._internal();
  static final NotificationService _instance = NotificationService._internal();

  /// Inicializa el servicio
  Future<void> initialize() async {
    debugPrint('🔔 [NotificationService] Inicializado correctamente.');
  }

  /// Cancela notificaciones existentes y programa una nueva
  Future<void> scheduleReminder(
      {required String title,
      required String body,
      required Duration delay}) async {
    debugPrint(
        '🔔 [NotificationService] Recordatorio programado para dentro de ${delay.inMinutes} minutos: "$title"');

    // Mock: Solo imprime el log cuando ocurre
    Timer(delay, () {
      debugPrint('🔔 [NotificationService] ¡Ping! $title - $body');
    });
  }

  /// Cancela todas las alarmas/notificaciones pendientes
  Future<void> cancelAll() async {
    debugPrint('🔔 [NotificationService] Todas las notificaciones canceladas.');
  }
}
