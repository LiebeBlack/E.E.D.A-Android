"""
Módulo: settings_manager.py
Propósito: Gestión centralizada de la configuración y el diálogo de ajustes.
"""

from typing import TYPE_CHECKING, Callable
import flet as ft

from core.theme import DesignTokens
from core.config import ThemePresets, ThemeModeType, config
from core.utils import safe_update, close_all_overlays

if TYPE_CHECKING:
    from main import App


class SettingsManager:
    """
    Gestor de configuración de la aplicación.
    
    Responsabilidades:
        - Construir el diálogo de ajustes (visitante y admin).
        - Manejar cambios de tema.
        - Manejar controles de audio.
        - Manejar intensidad de animaciones.
    """
    
    def __init__(self, app: "App") -> None:
        self.app = app
        self.page = app.app_page
        
    def show_settings(self, _: ft.ControlEvent | None = None) -> None:
        """Muestra el diálogo de ajustes según el modo (visitante/admin)."""
        protocol_color = DesignTokens.get_protocol_color(self.app.age_protocol)
        text_main = DesignTokens.get_text_main(self.app.age_protocol)
        text_dim = DesignTokens.get_text_dim(self.app.age_protocol)
        
        # Secciones comunes
        theme_section = self._build_theme_section(protocol_color, text_main, text_dim)
        audio_panel = self._build_audio_panel(protocol_color, text_main, text_dim)
        anim_panel = self._build_anim_panel(protocol_color, text_main, text_dim)
        dev_node = self._build_dev_node(protocol_color, text_main, text_dim)
        
        if self.app.is_admin:
            from core.admin_tools import AdminTools
            admin_tools = AdminTools(self.app)
            dialog_content = admin_tools.build_admin_panel(
                theme_section, audio_panel, anim_panel, dev_node
            )
            title_color = "#FFD600"
            title_text = "CONSOLA ADMIN E.E.D.A."
            title_icon = ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED
        else:
            dialog_content = self._build_visitor_content(
                protocol_color, text_main, text_dim,
                theme_section, audio_panel, anim_panel, dev_node
            )
            title_color = protocol_color
            title_text = "CONSOLA DE CONTROL E.E.D.A."
            title_icon = ft.Icons.SETTINGS_OUTLINED
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(title_icon, color=title_color, size=24),
                ft.Text(title_text, size=16, weight="bold"),
                ft.Container(expand=True),
                ft.IconButton(
                    ft.Icons.CLOSE_ROUNDED,
                    icon_color=text_dim,
                    icon_size=20,
                    on_click=lambda _: self.page.close(dialog),
                    tooltip="Cerrar"
                ),
            ], alignment="center", spacing=10),
            content=dialog_content,
            shape=ft.RoundedRectangleBorder(radius=20),
        )
        
        self.page.open(dialog)
    
    def _build_theme_section(
        self, protocol_color: str, text_main: str, text_dim: str
    ) -> ft.Container:
        """Sección de selección de tema."""
        
        # Referencias a controles de texto que necesitan actualización de color
        theme_labels: list[ft.Text] = []
        
        def change_theme(mode: ThemeModeType) -> None:
            new_theme = ft.Theme(font_family=config.font_main)
            
            theme_data = {
                "sunrise": (
                    ft.ThemeMode.LIGHT,
                    ThemePresets.sunrise(protocol_color),
                    "#000000",  # text_main
                    "#455A64",  # text_dim
                ),
                "rest": (
                    ft.ThemeMode.LIGHT,
                    ThemePresets.rest(protocol_color),
                    "#2D1B18",  # text_main - marrón oscuro para fondo ámbar
                    "#5D4037",  # text_dim - marrón medio
                ),
                "sleep": (
                    ft.ThemeMode.DARK,
                    ThemePresets.sleep(protocol_color),
                    "#FFFFFF",  # text_main - blanco para fondo oscuro
                    "#B0BEC5",  # text_dim - gris claro
                ),
            }
            
            theme_mode, colors, new_text_main, new_text_dim = theme_data.get(mode, theme_data["sunrise"])
            self.page.theme_mode = theme_mode
            
            # Guardar el tema actual para que otros módulos lo usen
            self.app.current_theme_mode = mode
            
            # Actualizar blobs
            for i, color in enumerate(colors.blob_colors):
                if i < len(self.app.blobs):
                    self.app.blobs[i].bgcolor = color
            
            new_theme.color_scheme = ft.ColorScheme(
                primary=protocol_color,
                surface=colors.surface_color,
                on_surface=colors.on_surface_color,
                on_surface_variant=colors.on_surface_variant,
                background=colors.bg_color,
            )
            
            if self.app._bg_container:
                self.app._bg_container.bgcolor = colors.bg_color
            
            self.page.theme = new_theme
            
            # Actualizar colores de texto en los controles del diálogo
            for label in theme_labels:
                label.color = new_text_dim
                
            safe_update(self.page)
        
        def make_theme_button(
            icon: str, color: str, mode: ThemeModeType, label_text: str, tooltip: str
        ) -> ft.Container:
            label = ft.Text(label_text, size=10, weight="bold", color=text_dim)
            theme_labels.append(label)
            return ft.Container(
                content=ft.Column([
                    ft.IconButton(
                        icon=getattr(ft.Icons, icon),
                        icon_color=color,
                        icon_size=28,
                        on_click=lambda _: change_theme(mode),
                        tooltip=tooltip,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            bgcolor=ft.Colors.with_opacity(0.08, color)
                        )
                    ),
                    label,
                ], horizontal_alignment="center", spacing=4)
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "AMBIENTE DE ILUMINACIÓN",
                    size=10,
                    weight="bold",
                    color=protocol_color,
                    font_family=config.font_mono
                ),
                ft.Container(height=8),
                ft.Row([
                    make_theme_button(
                        "WB_SUNNY_ROUNDED", ft.Colors.AMBER_600,
                        "sunrise", "Sunrise", "Modo claro"
                    ),
                    make_theme_button(
                        "COFFEE_ROUNDED", ft.Colors.ORANGE_400,
                        "rest", "Rest", "Modo descanso"
                    ),
                    make_theme_button(
                        "NIGHTS_STAY_ROUNDED", ft.Colors.INDIGO_300,
                        "sleep", "Sleep", "Modo oscuro"
                    ),
                ], alignment="center", spacing=30),
            ]),
            padding=16,
            bgcolor=ft.Colors.with_opacity(0.03, protocol_color),
            border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, protocol_color)),
        )
    
    def _build_audio_panel(
        self, protocol_color: str, text_main: str, text_dim: str
    ) -> ft.Container:
        """Panel de control de audio."""
        
        def on_master_change(e: ft.ControlEvent) -> None:
            self.app.master_volume = e.control.value
        
        def on_sfx_change(e: ft.ControlEvent) -> None:
            self.app.sfx_volume = e.control.value
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "CONTROL DE FRECUENCIAS (AUDIO)",
                    size=10,
                    weight="bold",
                    color=protocol_color,
                    font_family=config.font_mono
                ),
                ft.Container(height=8),
                ft.Row([
                    ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, size=16, color=protocol_color),
                    ft.Text("Volumen Maestro", size=12, expand=True, color=text_main),
                    ft.Slider(
                        min=0, max=1,
                        value=self.app.master_volume,
                        active_color=protocol_color,
                        width=180,
                        on_change=on_master_change
                    )
                ]),
                ft.Row([
                    ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, size=16, color=DesignTokens.COLORS["secondary"]),
                    ft.Text("Efectos SFX", size=12, expand=True, color=text_main),
                    ft.Slider(
                        min=0, max=1,
                        value=self.app.sfx_volume,
                        active_color=DesignTokens.COLORS["secondary"],
                        width=180,
                        on_change=on_sfx_change
                    )
                ])
            ], spacing=8),
            padding=16,
            bgcolor=ft.Colors.with_opacity(0.03, protocol_color),
            border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, protocol_color)),
        )
    
    def _build_anim_panel(
        self, protocol_color: str, text_main: str, text_dim: str
    ) -> ft.Container:
        """Panel de control de animaciones."""
        
        def on_anim_change(e: ft.ControlEvent) -> None:
            sel = e.control.selected
            if sel:
                self.app.anim_intensity = next(iter(sel))
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "DINÁMICA DE INTERFAZ",
                    size=10,
                    weight="bold",
                    color=protocol_color,
                    font_family=config.font_mono
                ),
                ft.Container(height=8),
                ft.SegmentedButton(
                    selected={self.app.anim_intensity},
                    on_change=on_anim_change,
                    segments=[
                        ft.Segment(value="Baja", label=ft.Text("Baja")),
                        ft.Segment(value="Media", label=ft.Text("Media")),
                        ft.Segment(value="Alta", label=ft.Text("Alta")),
                    ],
                )
            ]),
            padding=16,
            bgcolor=ft.Colors.with_opacity(0.03, protocol_color),
            border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, protocol_color)),
        )
    
    def _build_dev_node(
        self, protocol_color: str, text_main: str, text_dim: str
    ) -> ft.Container:
        """Nodo de información del desarrollador."""
        
        def launch_link(url: str) -> Callable[[ft.ControlEvent], None]:
            def handler(_: ft.ControlEvent) -> None:
                self.page.launch_url(url)
            return handler
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "NODO DE DESARROLLO CORE",
                    size=10,
                    weight="bold",
                    color=protocol_color,
                    font_family=config.font_mono
                ),
                ft.Container(height=8),
                ft.Row([
                    ft.Icon(ft.Icons.VERIFIED_USER_ROUNDED, color=DesignTokens.COLORS["accent"], size=18),
                    ft.Text("Yoangel Gómez (Liebe Black)", weight="bold", size=15, color=text_main),
                ], spacing=10),
                ft.Container(height=4),
                ft.Row([
                    ft.TextButton(
                        "GitHub",
                        icon=ft.Icons.CODE_ROUNDED,
                        on_click=launch_link("https://github.com/LiebeBlack/E.E.D.A-PC")
                    ),
                    ft.TextButton(
                        "Contacto",
                        icon=ft.Icons.EMAIL_ROUNDED,
                        on_click=launch_link("mailto:Liebeblack01@gmail.com")
                    ),
                ], spacing=5)
            ], spacing=2),
            padding=16,
            bgcolor=ft.Colors.with_opacity(0.04, protocol_color),
            border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, protocol_color)),
        )
    
    def _build_visitor_content(
        self, protocol_color: str, text_main: str, text_dim: str,
        theme_section: ft.Container,
        audio_panel: ft.Container,
        anim_panel: ft.Container,
        dev_node: ft.Container
    ) -> ft.Column:
        """Contenido del diálogo para modo visitante."""
        
        admin_input = ft.TextField(
            label="Clave de Desarrollador",
            password=True,
            can_reveal_password=True,
            text_size=12,
            border_radius=10,
            width=280,
            text_style=ft.TextStyle(font_family=config.font_mono)
        )
        status_text = ft.Text(
            "⬤ MODO VISITANTE",
            size=10,
            weight="bold",
            italic=True,
            color=text_dim
        )
        
        def validate_admin(_: ft.ControlEvent) -> None:
            pin = admin_input.value or ""
            if pin == config.admin_password:
                self.app.is_admin = True
                config.version.suffix = "ADMIN-UNLOCKED"
                close_all_overlays(self.page)
                self.show_settings(None)
                return
            else:
                status_text.value = "⬤ CLAVE INCORRECTA"
                status_text.color = DesignTokens.COLORS["critical"]
            safe_update(self.page)
        
        admin_input.on_submit = validate_admin
        
        admin_panel = ft.Container(
            content=ft.Column([
                ft.Text(
                    "SEGURIDAD DE NÚCLEO",
                    size=10,
                    weight="bold",
                    color=protocol_color,
                    font_family=config.font_mono
                ),
                ft.Container(height=8),
                ft.Row([
                    ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, size=14, color=text_dim),
                    status_text
                ]),
                ft.Row([
                    admin_input,
                    ft.ElevatedButton(
                        "Verificar",
                        icon=ft.Icons.LOCK_OPEN_ROUNDED,
                        on_click=validate_admin,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=12
                        ),
                    )
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ], spacing=10),
            padding=16,
            bgcolor=ft.Colors.with_opacity(0.03, protocol_color),
            border_radius=15,
            border=ft.border.all(1, ft.Colors.with_opacity(0.08, protocol_color)),
        )
        
        return ft.Column([
            theme_section,
            audio_panel,
            anim_panel,
            admin_panel,
            dev_node,
            ft.Container(height=8),
            ft.Row([
                ft.Text(
                    f"V {config.version}",
                    size=9,
                    weight="bold",
                    color=text_dim,
                    font_family=config.font_mono
                ),
                ft.Container(expand=True),
                ft.Text("E.E.D.A. — Ecosistema Educativo", size=10, italic=True, color=protocol_color),
            ])
        ], spacing=16, width=480, height=650, scroll=ft.ScrollMode.HIDDEN)
