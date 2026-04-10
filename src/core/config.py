"""
Módulo: config.py
Propósito: Configuración centralizada de la aplicación E.E.D.A.
Usa dataclasses y patrones modernos de Python 3.10+.
"""

from dataclasses import dataclass, field
from typing import Literal, Final
import flet as ft


# Tipos de protocolo
ProtocolType = Literal["alpha", "delta", "omega"]
ThemeModeType = Literal["sunrise", "rest", "sleep"]
AnimIntensityType = Literal["Baja", "Media", "Alta"]


@dataclass
class AppVersion:
    """Versión semántica de la aplicación."""
    major: int = 7
    minor: int = 3
    patch: int = 9
    suffix: str = "STABLE"
    
    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}-{self.suffix}"


@dataclass
class AppConfig:
    """Configuración global de la aplicación."""
    
    # Versionado
    version: AppVersion = field(default_factory=lambda: AppVersion())
    
    # Configuración de audio
    master_volume: float = 0.8
    sfx_volume: float = 0.5
    
    # Configuración de UI
    anim_intensity: AnimIntensityType = "Media"
    
    # Configuración de admin
    admin_password: str = "aidmind"
    
    # Títulos de la aplicación
    app_title: str = "E.E.D.A. — Ecosistema Educativo Digital Adaptable"
    window_title: str = "E.E.D.A. - Ecosistema Educativo Digital Adaptable"
    
    # Fuentes
    font_mono: str = "JetBrains Mono"
    font_main: str = "Inter"
    font_display: str = "Lexend"


@dataclass(frozen=True)
class ThemeColors:
    """Colores del tema por modo."""
    bg_color: str
    blob_colors: list[str]
    surface_color: str
    on_surface_color: str
    on_surface_variant: str


class ThemePresets:
    """Presets de temas predefinidos."""
    
    @staticmethod
    def sunrise(primary: str) -> ThemeColors:
        return ThemeColors(
            bg_color="#FFFFFF",
            blob_colors=[
                ft.Colors.with_opacity(0.18, primary),
                ft.Colors.with_opacity(0.12, "#00B8FF"),
                ft.Colors.with_opacity(0.10, ft.Colors.PURPLE_200),
                ft.Colors.with_opacity(0.08, ft.Colors.CYAN_200),
            ],
            surface_color="#FFFFFF",
            on_surface_color="#000000",
            on_surface_variant="#455A64",
        )
    
    @staticmethod
    def rest(primary: str) -> ThemeColors:
        return ThemeColors(
            bg_color="#FFF9E6",
            blob_colors=[
                ft.Colors.with_opacity(0.28, ft.Colors.AMBER_400),
                ft.Colors.with_opacity(0.18, ft.Colors.ORANGE_400),
                ft.Colors.with_opacity(0.15, ft.Colors.DEEP_ORANGE_200),
                ft.Colors.with_opacity(0.12, ft.Colors.YELLOW_500),
            ],
            surface_color="#FFF9E6",
            on_surface_color="#2D1B18",
            on_surface_variant="#5D4037",
        )
    
    @staticmethod
    def sleep(primary: str) -> ThemeColors:
        return ThemeColors(
            bg_color="#0A0A12",
            blob_colors=[
                ft.Colors.with_opacity(0.25, ft.Colors.BLUE_ACCENT_700),
                ft.Colors.with_opacity(0.18, ft.Colors.PURPLE_ACCENT_400),
                ft.Colors.with_opacity(0.15, ft.Colors.CYAN_500),
                ft.Colors.with_opacity(0.12, ft.Colors.PINK_400),
            ],
            surface_color="#0A0A12",
            on_surface_color="#FFFFFF",
            on_surface_variant="#B0BEC5",
        )


# Constantes globales
GOLD_ACCENT: Final[str] = "#00B4D8"
MODULE_NAMES: Final[dict[str, str]] = {
    "dashboard": "Dashboard",
    "zones": "Zones",
    "security": "Security",
    "lab": "Lab",
}

# Configuración de blobs de fondo
BLOB_COUNT: Final[int] = 4
BLOB_ANIMATION_DURATION: Final[int] = 8000  # ms
BLOB_UPDATE_INTERVAL: Final[float] = 8.0  # segundos

# Configuración de secuencia de arranque
BOOT_SEQUENCE_DELAY: Final[float] = 0.55  # segundos entre logs
BOOT_FINAL_DELAY: Final[float] = 0.45  # segundos antes de mostrar protocolos


# Instancia global de configuración
config = AppConfig()
