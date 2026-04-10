"""
Módulo: main.py
Propósito: Punto de entrada y controlador principal de la aplicación E.E.D.A.
Archivo desarrollado por Yoangel Gómez

Versión refactorizada usando arquitectura modular moderna.
"""

from __future__ import annotations

import asyncio
import random
from typing import TYPE_CHECKING

import flet as ft

from core.event_bus import bus
from core.theme import DesignTokens
from core.config import (
    config,
    ProtocolType,
    BLOB_ANIMATION_DURATION,
    BLOB_UPDATE_INTERVAL,
    BOOT_SEQUENCE_DELAY,
    BOOT_FINAL_DELAY,
)
from core.utils import safe_page_update
from core.settings_manager import SettingsManager
from components.sidebar import Sidebar
from modules.dashboard import Dashboard
from modules.zones import Zones
from modules.security import Security
from modules.lab import Lab

if TYPE_CHECKING:
    from flet import Page


class App(ft.Container):
    """
    Controlador principal de la aplicación E.E.D.A.
    (Ecosistema Educativo Digital Adaptable)
    
    Responsabilidades:
        1. Configurar la página (tema, fuentes, fondo).
        2. Mostrar la secuencia de arranque pedagógica.
        3. Gestionar la selección de protocolo por edad.
        4. Construir el layout principal (Sidebar + área de contenido).
        5. Centralizar la navegación entre módulos con limpieza de recursos.
    """

    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.app_page = page
        self.expand = True
        
        # Estado de protocolo
        self.age_protocol: ProtocolType | None = None
        self.sidebar: Sidebar | None = None
        self.active_module_instance = None
        self.current_module_container = ft.Container(
            expand=True,
            animate_opacity=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            opacity=1,
        )

        # Configuración Maestro y Estado del Sistema
        self.master_volume: float = config.master_volume
        self.sfx_volume: float = config.sfx_volume
        self.anim_intensity: str = config.anim_intensity
        self.is_admin: bool = False
        self.current_theme_mode: str = "sunrise"  # Tema por defecto

        # Estado de telemetría y navegación
        self._current_module: str | None = None
        self._nav_history: list[str] = []

        # Referencia al fondo dinámico
        self._bg_container: ft.Container | None = None
        self._blob_running: bool = False

        self._setup_page()
        self.show_initialization()

    # ──────────────────────────────────────────────────────────────────────────
    # CONFIGURACIÓN DE PÁGINA
    # ──────────────────────────────────────────────────────────────────────────

    def _setup_page(self) -> None:
        """Aplica el tema global, fuentes y colores base a la página."""
        p = self.app_page
        p.title = config.app_title
        p.padding = 0
        p.spacing = 0
        p.theme_mode = ft.ThemeMode.LIGHT
        p.bgcolor = None
        p.fonts = DesignTokens.FONTS

        # Elementos para el Fondo Líquido Dinámico
        self.blobs = [
            ft.Container(
                width=600, height=600, border_radius=300,
                bgcolor=ft.Colors.with_opacity(0.20, DesignTokens.COLORS["primary"]),
                blur=ft.Blur(120, 120),
                left=-150, top=-150,
                animate_offset=ft.Animation(BLOB_ANIMATION_DURATION, "easeInOutSine")
            ),
            ft.Container(
                width=700, height=700, border_radius=350,
                bgcolor=ft.Colors.with_opacity(0.15, DesignTokens.COLORS["secondary"]),
                blur=ft.Blur(140, 140),
                right=-200, bottom=-200,
                animate_offset=ft.Animation(int(BLOB_ANIMATION_DURATION * 1.3), "easeInOutSine")
            ),
            ft.Container(
                width=500, height=500, border_radius=250,
                bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.PURPLE_400),
                blur=ft.Blur(100, 100),
                left=200, bottom=50,
                animate_offset=ft.Animation(int(BLOB_ANIMATION_DURATION * 1.6), "easeInOutSine")
            ),
            ft.Container(
                width=450, height=450, border_radius=225,
                bgcolor=ft.Colors.with_opacity(0.10, ft.Colors.CYAN_400),
                blur=ft.Blur(90, 90),
                right=100, top=100,
                animate_offset=ft.Animation(int(BLOB_ANIMATION_DURATION * 1.4), "easeInOutSine")
            ),
        ]

        p.theme = ft.Theme(
            font_family=config.font_main,
            visual_density=ft.VisualDensity.COMPACT,
            color_scheme=ft.ColorScheme(
                primary=DesignTokens.COLORS["primary"],
                secondary=DesignTokens.COLORS["secondary"],
            ),
        )

    # ──────────────────────────────────────────────────────────────────────────
    # PANTALLA DE ARRANQUE
    # ──────────────────────────────────────────────────────────────────────────

    def show_initialization(self) -> None:
        """Muestra la pantalla de arranque con la secuencia de logs de terminal."""
        terminal_text = ft.Text(
            "",
            font_family=config.font_mono,
            color=DesignTokens.COLORS["primary"],
            size=12,
        )

        self.content = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.SMART_TOY_OUTLINED, size=56, color=DesignTokens.COLORS["primary"]),
                    ft.Text(
                        "E.E.D.A. — Iniciando Sistema",
                        size=22,
                        weight="bold",
                        font_family=config.font_mono,
                        color=DesignTokens.get_text_main("alpha")
                    ),
                    ft.Divider(color=DesignTokens.COLORS["primary"], height=2, thickness=2),
                    terminal_text,
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=20,
            ),
            alignment=ft.Alignment(0, 0),
            padding=50,
        )

        self.app_page.update()
        self.app_page.run_task(self._run_boot_sequence, terminal_text)

    async def _run_boot_sequence(self, terminal_text: ft.Text) -> None:
        """Secuencia de arranque asíncrona (~3.5 s total)."""
        boot_logs = [
            f"> Iniciando sistema E.E.D.A. {config.version}...",
            "> Cargando protocolos de aprendizaje...",
            "> Estableciendo entorno seguro...",
            "> Indexando contenido educativo...",
            "> Todo listo. Selecciona tu nivel para comenzar.",
        ]

        for log in boot_logs:
            terminal_text.value += f"\n{log}"
            safe_page_update(self.app_page)
            await asyncio.sleep(BOOT_SEQUENCE_DELAY)

        await asyncio.sleep(BOOT_FINAL_DELAY)
        self.show_protocol_selection()

    # ──────────────────────────────────────────────────────────────────────────
    # SELECCIÓN DE PROTOCOLO
    # ──────────────────────────────────────────────────────────────────────────

    def show_protocol_selection(self) -> None:
        """Muestra las tarjetas de selección de Protocolo (Alpha / Delta / Omega)."""

        def select_protocol(protocol: ProtocolType) -> None:
            self.age_protocol = protocol
            p_color = DesignTokens.get_protocol_color(protocol)
            self.app_page.theme = ft.Theme(
                font_family=config.font_main,
                color_scheme=ft.ColorScheme(primary=p_color)
            )
            self.build_main_layout()
            self.navigate_to("zones")

        protocol_cards_data = [
            {
                "id": "alpha",
                "icon": ft.Icons.ROCKET_LAUNCH,
                "title": "Nivel Alpha",
                "age": "3 a 7 años",
                "desc": "Explora el mundo digital con juegos y colores.",
                "color": DesignTokens.COLORS["primary"]
            },
            {
                "id": "delta",
                "icon": ft.Icons.TERMINAL,
                "title": "Nivel Delta",
                "age": "8 a 12 años",
                "desc": "Aprende lógica, redes y herramientas digitales.",
                "color": DesignTokens.COLORS["secondary"]
            },
            {
                "id": "omega",
                "icon": ft.Icons.SHIELD_MOON,
                "title": "Nivel Omega",
                "age": "13 a 16 años",
                "desc": "Diseña sistemas y domina herramientas avanzadas.",
                "color": DesignTokens.COLORS["critical"]
            },
        ]

        cards = []
        for card in protocol_cards_data:
            cards.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(card["icon"], size=52, color=card["color"]),
                            ft.Text(card["title"], weight="bold", size=18,
                                   color=DesignTokens.get_text_main("alpha")),
                            ft.Text(card["age"], size=16, weight="bold", color=card["color"]),
                            ft.Text(card["desc"], size=11, italic=True,
                                   color=DesignTokens.get_text_dim("alpha"), text_align="center"),
                        ],
                        horizontal_alignment="center",
                        spacing=8,
                    ),
                    on_click=lambda _, p=card["id"]: select_protocol(p),
                    width=230, height=260, padding=30,
                    border=ft.border.all(1, DesignTokens.get_glass_border(card["id"])),
                    border_radius=20,
                    bgcolor=ft.Colors.with_opacity(0.05, card["color"]),
                    ink=True,
                    animate_scale=ft.Animation(250, ft.AnimationCurve.DECELERATE),
                    on_hover=lambda e: self._on_card_hover(e),
                )
            )

        self.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Ecosistema Educativo Digital Adaptable",
                        size=13,
                        color=DesignTokens.get_text_dim("alpha"),
                        font_family=config.font_mono,
                        weight="bold"
                    ),
                    ft.Text("¿Cuántos años tienes?", size=32, weight="bold",
                           color=DesignTokens.get_text_main("alpha")),
                    ft.Container(height=30),
                    ft.Row(cards, alignment="center", spacing=30, wrap=True),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            alignment=ft.Alignment(0, 0),
        )
        self.app_page.update()

    def _on_card_hover(self, e: ft.HoverEvent) -> None:
        """Efecto de escala al hacer hover sobre las tarjetas de protocolo."""
        e.control.scale = 1.06 if e.data == "true" else 1.0
        e.control.update()

    # ──────────────────────────────────────────────────────────────────────────
    # CONSOLA DE CONTROL (SETTINGS)
    # ──────────────────────────────────────────────────────────────────────────

    def show_settings(self, e: ft.ControlEvent | None) -> None:
        """Muestra el diálogo de ajustes."""
        SettingsManager(self).show_settings(e)

    # ──────────────────────────────────────────────────────────────────────────
    # LAYOUT PRINCIPAL
    # ──────────────────────────────────────────────────────────────────────────

    def build_main_layout(self) -> None:
        """Construye el layout Sidebar + área de contenido tras seleccionar protocolo."""
        self.sidebar = Sidebar(
            on_nav_change=self.navigate_to,
            on_home=self.show_protocol_selection,
            protocol=self.age_protocol,
        )

        settings_button = ft.Container(
            content=ft.Row(
                [
                    ft.Container(expand=True),
                    ft.IconButton(
                        ft.Icons.SETTINGS_ROUNDED,
                        icon_size=28,
                        icon_color=DesignTokens.get_protocol_color(self.age_protocol),
                        tooltip="Ajustes y Más Opciones",
                        on_click=self.show_settings,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            bgcolor=ft.Colors.with_opacity(
                                0.06, DesignTokens.get_protocol_color(self.age_protocol)
                            ),
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            padding=ft.padding.only(top=10, right=20)
        )

        initial_bg = "#FFFFFF" if self.app_page.theme_mode == ft.ThemeMode.LIGHT else "#0A0A12"

        self._bg_container = ft.Container(
            content=ft.Stack(self.blobs),
            expand=True,
            bgcolor=initial_bg,
        )

        self.content = ft.Stack(
            [
                self._bg_container,
                ft.Row(
                    controls=[
                        self.sidebar,
                        ft.Column(
                            [
                                settings_button,
                                ft.Container(
                                    content=self.current_module_container,
                                    expand=True,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                )
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True,
                    spacing=0,
                )
            ],
            expand=True
        )
        self.app_page.update()

        if not self._blob_running:
            self._blob_running = True
            self.app_page.run_task(self._animate_blobs_async)

    async def _animate_blobs_async(self) -> None:
        """Animación asíncrona de blobs — usa asyncio en lugar de threading."""
        while self._blob_running:
            for blob in self.blobs:
                blob.offset = ft.Offset(
                    random.uniform(-0.15, 0.25),
                    random.uniform(-0.15, 0.25)
                )
            safe_page_update(self.app_page)
            await asyncio.sleep(BLOB_UPDATE_INTERVAL)

    # ──────────────────────────────────────────────────────────────────────────
    # NAVEGACIÓN CENTRALIZADA
    # ──────────────────────────────────────────────────────────────────────────

    def navigate_to(self, module_name: str) -> None:
        """Navega al módulo indicado, limpiando el anterior."""
        module_map = {
            "dashboard": Dashboard,
            "zones": Zones,
            "security": Security,
            "lab": Lab,
        }

        module_class = module_map.get(module_name)
        if module_class:
            module = module_class(navigation_manager=self, protocol=self.age_protocol)
        else:
            module = ft.Container(
                content=ft.Text(
                    f"Módulo '{module_name}' en desarrollo.",
                    font_family=config.font_mono,
                    color=DesignTokens.get_text_dim(self.age_protocol)
                ),
                alignment=ft.Alignment(0, 0),
            )

        if self.active_module_instance and hasattr(self.active_module_instance, "cleanup"):
            self.active_module_instance.cleanup()

        self.current_module_container.opacity = 0
        safe_page_update(self.app_page)

        self.active_module_instance = module
        self.current_module_container.content = module
        self.current_module_container.opacity = 1

        # Registrar en historial de navegación
        self._nav_history.append(module_name)

        if self.sidebar:
            self.sidebar.set_active(module_name)

        bus.emit("nav_change", module_name)
        safe_page_update(self.app_page)


# ──────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ──────────────────────────────────────────────────────────────────────────────

def main(page: ft.Page) -> None:
    """Función de entrada principal requerida por Flet."""
    page.title = config.window_title
    page.theme_mode = ft.ThemeMode.LIGHT
    app = App(page)
    page.add(app)


if __name__ == "__main__":
    ft.app(target=main)
