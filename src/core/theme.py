"""
Módulo: theme.py
Archivo desarrollado por Yoangel Gómez
"""

import flet as ft

# Tipo alias para mayor claridad en type hints
Protocol = str  # "alpha" | "delta" | "omega"


class DesignTokens:
    """
    Sistema de tokens de diseño centralizado.
    Adapta colores, tipografía y espaciado según el Protocolo activo (edad del usuario).

    Protocolos:
        - alpha  → 3–7  años → Verde  (#00C853) → Lúdico, simple
        - delta  → 8–12 años → Azul   (#00B0FF) → Técnico introductorio
        - omega  → 13–16 años → Naranja/Rojo (#FF3D00) → Técnico avanzado / hacker
    """

    # ──────────────────────────────────────────────────────────────────────────
    # PALETA DE COLORES GLOBAL (sin hardcodear en otros módulos)
    # ──────────────────────────────────────────────────────────────────────────
    COLORS: dict[str, str] = {
        # Colores de Protocolo Saturados y Fuertes
        "primary":   "#00D859",  # Verde Alpha más vibrante
        "secondary": "#00B8FF",  # Azul Delta más profundo
        "critical":  "#FF4D00",  # Rojo Omega más intenso

        # Colores de Estado
        "accent":    "#2E7D32",  # Verde oscuro — Éxito / Seguro
        "warning":   "#FFD600",  # Amarillo      — Precaución
        "tertiary":  "#6200EA",  # Púrpura       — Quiz / Evaluación

        # Colores de Superficie
        "bg_dark":   "#F0F4F0",  # Gris-verde claro — Fondo general
        "bg_panel":  "#FFFFFF",  # Blanco           — Paneles / Tarjetas

        # Colores de Soporte
        "vibrant_pink": "#FF4081",
        "vibrant_cyan": "#00E5FF",
        "glass":         "rgba(255, 255, 255, 0.7)",
    }

    # ──────────────────────────────────────────────────────────────────────────
    # TIPOGRAFÍA — Fuentes registradas para Flet Desktop
    # ──────────────────────────────────────────────────────────────────────────
    FONTS: dict[str, str] = {
        "JetBrains Mono": (
            "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/"
            "JetBrainsMono-Regular.ttf"
        ),
        "Inter": (
            "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.otf"
        ),
        "Lexend": (
            "https://github.com/googlefonts/lexend/raw/main/fonts/lexend/ttf/Lexend-Regular.ttf"
        ),
    }

    # ──────────────────────────────────────────────────────────────────────────
    # GLASSMORPHISM — Estilo base para contenedores glass
    # ──────────────────────────────────────────────────────────────────────────
    GLASS_STYLE: dict[str, int | float] = {
        "blur":          30,
        "opacity":       0.1,
        "border_radius": 20,
    }

    # ──────────────────────────────────────────────────────────────────────────
    # MÉTODOS DE UTILIDAD
    # ──────────────────────────────────────────────────────────────────────────

    @staticmethod
    def get_spacing(n: int) -> float:
        """
        Devuelve un valor de espaciado basado en la Proporción Áurea.
        Fórmula: S = 10 × 1.618ⁿ  (Incrementado de 8 a 10 para más espacio)
        """
        return 10 * (1.618 ** n)

    @classmethod
    def get_protocol_color(cls, protocol: Protocol) -> str:
        """
        Retorna el color principal del protocolo activo.

        Args:
            protocol: Identificador del protocolo ("alpha", "delta", "omega").

        Returns:
            Código hexadecimal de color.
        """
        mapping: dict[str, str] = {
            "alpha": cls.COLORS["primary"],
            "delta": cls.COLORS["secondary"],
            "omega": cls.COLORS["critical"],
        }
        return mapping.get(protocol, cls.COLORS["primary"])

    @classmethod
    def get_text_main(cls, protocol: Protocol) -> str:
        """
        Color de texto principal — Adaptativo al Modo de Tema (Flet ON_SURFACE).
        """
        return ft.Colors.ON_SURFACE

    @classmethod
    def get_text_dim(cls, protocol: Protocol) -> str:
        """
        Color de texto secundario — Adaptativo (Flet ON_SURFACE_VARIANT).
        """
        return ft.Colors.ON_SURFACE_VARIANT

    @classmethod
    def get_glass_bg(cls, protocol: Protocol) -> ft.Colors:
        """
        Fondo semitransparente más sólido (0.15) para mejor legibilidad.
        """
        color = cls.get_protocol_color(protocol)
        return ft.Colors.with_opacity(0.15, color)

    @classmethod
    def get_glass_border(cls, protocol: Protocol) -> ft.Colors:
        """
        Borde semitransparente para contenedores Glassmorphism.
        """
        color = cls.get_protocol_color(protocol)
        return ft.Colors.with_opacity(0.15, color)

    @classmethod
    def get_premium_gradient(cls, protocol: Protocol) -> ft.LinearGradient:
        """
        Gradiente diagonal premium, basado en el color del protocolo activo.
        Usar para fondos de tarjetas o secciones destacadas.
        """
        color = cls.get_protocol_color(protocol)
        return ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[
                ft.Colors.with_opacity(0.15, color),
                ft.Colors.with_opacity(0.05, color),
            ],
        )

    @classmethod
    def get_active_nav_gradient(cls, protocol: Protocol) -> ft.LinearGradient:
        """
        Gradiente horizontal para el ítem de navegación activo en el Sidebar.
        """
        color = cls.get_protocol_color(protocol)
        return ft.LinearGradient(
            begin=ft.Alignment(-1, 0),
            end=ft.Alignment(1, 0),
            colors=[
                ft.Colors.with_opacity(0.18, color),
                ft.Colors.with_opacity(0.03, color),
            ],
        )
