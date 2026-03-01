import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:isla_digital/core/services/services.dart';
import 'package:isla_digital/core/theme/app_theme.dart';
import 'package:isla_digital/core/utils/page_transitions.dart';
import 'package:isla_digital/presentation/providers/app_providers.dart';
import 'package:isla_digital/presentation/views/screens/home_screen.dart';
import 'package:isla_digital/presentation/views/screens/level_select_screen.dart';
import 'package:isla_digital/presentation/views/screens/parental_dashboard_screen.dart';
import 'package:isla_digital/presentation/views/screens/profile_setup_screen.dart';
import 'package:isla_digital/presentation/views/screens/showcase_screen.dart';
import 'package:isla_digital/presentation/widgets/island_background.dart';

void main() async {
  // 1. Asegurar inicialización de bindings
  WidgetsFlutterBinding.ensureInitialized();

  // 2. Inicialización de servicios con manejo de errores más descriptivo
  try {
    await Future.wait([
      LocalStorageService.initialize(),
      BackgroundMusicService.initialize(),
    ]);
  } catch (e, stackTrace) {
    debugPrint('Error crítico en inicialización: $e');
    debugPrint(stackTrace.toString());
    // Aquí podrías añadir una lógica para mostrar una pantalla de error si falla algo vital
  }

  runApp(
    const ProviderScope(
      child: IslaDigitalApp(),
    ),
  );
}

class IslaDigitalApp extends ConsumerWidget {
  const IslaDigitalApp({super.key});

  // Centralizamos las rutas en constantes para evitar errores de escritura (Typo)
  static const String routeHome = '/home';
  static const String routeProfile = '/profile';
  static const String routeLevels = '/levels';
  static const String routeParental = '/parental';
  static const String routeShowcase = '/showcase';

  static final Map<String, Widget Function()> _routes = {
    routeHome: () => const HomeScreen(),
    routeProfile: () => const ProfileSetupScreen(),
    routeLevels: () => const LevelSelectScreen(),
    routeParental: () => const ParentalDashboardScreen(),
    routeShowcase: () => const ShowcaseScreen(),
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Escuchamos el estado del perfil
    final profile = ref.watch(currentProfileProvider);

    return MaterialApp(
      title: 'Isla Digital',
      debugShowCheckedModeBanner: false,
      theme: IslaThemes.lightTheme,
      // Lógica de redirección inicial más clara
      initialRoute: profile == null ? routeProfile : routeHome,
      
      // Optimizamos el Builder para el fondo global
      builder: (context, child) {
        return Scaffold(
          resizeToAvoidBottomInset: false, // Evita que el teclado mueva el fondo
          body: Stack(
            children: [
              const IslandBackground(), 
              if (child != null) child,
            ],
          ),
        );
      },
      
      onGenerateRoute: (settings) {
        final builder = _routes[settings.name];
        if (builder != null) {
          return FadeSlideRoute(page: builder());
        }
        
        // Pantalla de error 404 estéticamente acorde al tema
        return MaterialPageRoute(
          builder: (_) => Scaffold(
            appBar: AppBar(title: const Text('Error')),
            body: const Center(child: Text('La página solicitada no existe.')),
          ),
        );
      },
    );
  }
}