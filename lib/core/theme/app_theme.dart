import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class IslaColors {
  // Primarios
  static const Color oceanBlue = Color(0xFF1E90FF); 
  static const Color oceanLight = Color(0xFF64B5F6);
  static const Color oceanDark = Color(0xFF0D47A1);
  static const Color sunflower = Color(0xFFFFD700); 
  static const Color tropicOrange = Color(0xFFFF8C00); // FIX: Agregado
  
  // Acentuados (Requeridos por los niveles)
  static const Color jungleGreen = Color(0xFF00C853); 
  static const Color leafLight = Color(0xFF69F0AE);
  static const Color sunsetPink = Color(0xFFFF4081);   // FIX: Agregado
  static const Color royalPurple = Color(0xFF7C4DFF);  // FIX: Agregado
  static const Color coralReef = Color(0xFFFF5252);
  
  // Neutros y UI
  static const Color charcoal = Color(0xFF0F172A); 
  static const Color slate = Color(0xFF64748B);        // FIX: Agregado
  static const Color softWhite = Color(0xFFF8FAFC);
  static const Color white = Colors.white;
  static const Color black = Colors.black;             // FIX: Agregado
  static const Color grey = Colors.grey;               // FIX: Agregado
  static const Color greyLight = Color(0xFFF1F5F9);
  static const Color mist = Color(0xFFE2E8F0);
  static const Color sand = Color(0xFFFBE9E7);
}

class IslaTypography {
  static TextTheme get textTheme {
    return GoogleFonts.outfitTextTheme().copyWith(
      displayLarge: GoogleFonts.outfit(
        fontSize: 48, 
        fontWeight: FontWeight.w900, // FIX: Cambiado de .black a .w900
        color: IslaColors.charcoal,
        letterSpacing: -2,
      ),
      displayMedium: GoogleFonts.outfit(
        fontSize: 36, 
        fontWeight: FontWeight.w900, 
        color: IslaColors.charcoal,
      ),
      bodyLarge: GoogleFonts.outfit(
        fontSize: 20, 
        fontWeight: FontWeight.w600, 
        color: IslaColors.charcoal,
        height: 1.4,
      ),
      labelLarge: GoogleFonts.outfit(
        fontSize: 18, 
        fontWeight: FontWeight.w800, 
        letterSpacing: 1.1,
      ),
    );
  }
}

class IslaThemes {
  // FIX: Agregados getters de estilo que 'home_screen.dart' está pidiendo
  static TextStyle get labelStyle => GoogleFonts.outfit(fontSize: 14, fontWeight: FontWeight.w600, color: IslaColors.slate);
  static TextStyle get titleMediumStyle => GoogleFonts.outfit(fontSize: 18, fontWeight: FontWeight.w700, color: IslaColors.charcoal);
  static TextStyle get badgeCounterStyle => GoogleFonts.outfit(fontSize: 12, fontWeight: FontWeight.w800, color: IslaColors.white);
  static TextStyle get displayStyle => GoogleFonts.outfit(fontSize: 28, fontWeight: FontWeight.w900, color: IslaColors.charcoal);
  static TextStyle get subtitleStyle => GoogleFonts.outfit(fontSize: 16, fontWeight: FontWeight.w500, color: IslaColors.slate);

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: IslaColors.oceanBlue,
        primary: IslaColors.oceanBlue,
        secondary: IslaColors.sunflower,
        surface: IslaColors.softWhite,
        error: IslaColors.coralReef,
      ),
      textTheme: IslaTypography.textTheme,
      
      sliderTheme: SliderThemeData(
        activeTrackColor: IslaColors.oceanBlue,
        inactiveTrackColor: IslaColors.mist,
        thumbColor: IslaColors.oceanBlue,
        overlayColor: IslaColors.oceanBlue.withValues(alpha: 0.1),
        trackHeight: 8,
        thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 14),
      ),

      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: IslaColors.oceanBlue,
          foregroundColor: Colors.white,
          minimumSize: const Size(180, 72), 
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
          elevation: 4,
          shadowColor: IslaColors.oceanBlue.withValues(alpha: 0.4),
        ),
      ),

      dialogTheme: DialogThemeData(
        backgroundColor: Colors.white.withValues(alpha: 0.85),
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(40),
          side: const BorderSide(color: Colors.white, width: 2),
        ),
      ),
    );
  }
}

// Extension para facilitar el acceso
extension IslaColorScheme on BuildContext {
  ColorScheme get colors => Theme.of(this).colorScheme;
  TextTheme get text => Theme.of(this).textTheme;
}