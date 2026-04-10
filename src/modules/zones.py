"""
Módulo: zones.py
Archivo desarrollado por Yoangel Gómez
Propósito: Mapa de unidades educativas — lista y vista de detalle.
Política (Cot.md): Usa ContentEngine para el contenido y db (database) para el progreso.
Sin acceso directo a SQLite. Sin valores hardcoded de color o texto.
"""

import flet as ft

from base.module import BaseModule
from core.theme import DesignTokens
from core.content import ContentEngine
from core.database import db
from components.glass_container import GlassContainer
from components.technical_diagram import TechnicalDiagram


class Zones(BaseModule):
    """
    Módulo Zones — Mapa de unidades pedagógicas con dos vistas:
        1. List view: cuadrícula/lista de todas las unidades disponibles.
        2. Detail view: contenido completo de una unidad (intro, diagrama, desafío, quiz).

    Adapta títulos y subtítulos al protocolo activo (alpha/delta/omega).
    Guarda respuestas y progreso a través de la capa de persistencia centralizada (db).
    """

    def __init__(self, navigation_manager=None, protocol: str = "alpha") -> None:
        super().__init__(navigation_manager, protocol)
        self.protocol_data   = ContentEngine.PROTOCOLS.get(protocol, ContentEngine.PROTOCOLS["alpha"])
        self.units           = ContentEngine.get_all_units(protocol)
        self.current_view    = "list"  # "list" | "detail"
        self.selected_unit   = None
        self.immersive_mode  = False

        self.challenge_input = ft.TextField(
            label="TU RESPUESTA O REFLEXIÓN",
            multiline=True,
            min_lines=3,
            border_color=DesignTokens.get_glass_border(protocol),
            focused_border_color=DesignTokens.COLORS["accent"],
            cursor_color=DesignTokens.get_protocol_color(protocol),
            label_style=ft.TextStyle(
                color=DesignTokens.get_text_dim(protocol),
                weight="bold",
            ),
            text_style=ft.TextStyle(
                color=DesignTokens.get_text_main(protocol)
            ),
            bgcolor=ft.Colors.with_opacity(
                0.05, DesignTokens.get_protocol_color(protocol)
            ),
        )
        self.initialize()

    # ──────────────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN — DESPACHADOR DE VISTAS
    # ──────────────────────────────────────────────────────────────────────────

    def build(self) -> ft.Control:
        if self.current_view == "list":
            return self._build_list_view()
        return self._build_detail_view()

    # ──────────────────────────────────────────────────────────────────────────
    # VISTA DE LISTA
    # ──────────────────────────────────────────────────────────────────────────

    def _build_list_view(self) -> ft.Column:
        title_color = DesignTokens.get_protocol_color(self.protocol)
        completed   = db.get_progress(self.protocol)

        titles = {
            "alpha": "Mis Aventuras",
            "delta": "Temas de Aprendizaje",
            "omega": "Mapa del Conocimiento",
        }
        header = ft.Row(
            [
                ft.Text(
                    titles.get(self.protocol, "Temas"),
                    size=20,
                    font_family="JetBrains Mono",
                    weight=ft.FontWeight.BOLD,
                    color=title_color,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text(
                        f"{len(completed)}/{len(self.units)} completados",
                        size=11,
                        weight="bold",
                        color=DesignTokens.COLORS["accent"],
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=5),
                    bgcolor=ft.Colors.with_opacity(0.1, DesignTokens.COLORS["accent"]),
                    border_radius=20,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, DesignTokens.COLORS["accent"])),
                ),
            ]
        )

        units_grid = ft.GridView(
            expand=True,
            runs_count=2,
            max_extent=450, # Un poco más ancho
            child_aspect_ratio=3.2, # Proporción más cómoda
            spacing=25, # Más espacio entre tarjetas
            run_spacing=25,
            controls=[
                self._create_unit_card(unit, unit["id"] in completed)
                for unit in self.units
            ],
        )

        return ft.Column(
            controls=[
                header,
                ft.Divider(height=14, color=DesignTokens.get_glass_border(self.protocol)),
                units_grid,
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
        )

    def _stat_chip(self, icon, label: str, color: str) -> ft.Container:
        """Chip de estadística con icono, texto y fondo semitransparente."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=14, color=color),
                    ft.Text(
                        label,
                        size=11,
                        weight="bold",
                        color=DesignTokens.get_text_main(self.protocol),
                    ),
                ],
                spacing=5,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            bgcolor=ft.Colors.with_opacity(0.1, color),
            border_radius=20,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
        )

    def _create_unit_card(self, unit: dict, completed: bool) -> ft.Container:
        """Tarjeta compacta de unidad pedagógica."""
        protocol_color = DesignTokens.get_protocol_color(self.protocol)
        card_color     = DesignTokens.COLORS["accent"] if completed else protocol_color
        card_icon      = (
            ft.Icons.CHECK_CIRCLE
            if completed
            else getattr(ft.Icons, unit.get("icon", "BOOK"), ft.Icons.BOOK)
        )
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(card_icon, color=card_color, size=22),
                    ft.Column(
                        [
                            ft.Text(
                                unit["title"],
                                size=13,
                                weight="bold",
                                color=DesignTokens.get_text_main(self.protocol),
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                    ft.Icon(
                        ft.Icons.ARROW_FORWARD_IOS,
                        size=14,
                        color=ft.Colors.with_opacity(0.4, protocol_color),
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            border=ft.border.all(
                1,
                DesignTokens.COLORS["accent"] if completed
                else DesignTokens.get_glass_border(self.protocol),
            ),
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(
                0.12 if completed else 0.04, card_color
            ),
            on_click=lambda _, u=unit: self._open_unit_detail(u),
            ink=True,
        )

    # ──────────────────────────────────────────────────────────────────────────
    # VISTA DE DETALLE
    # ──────────────────────────────────────────────────────────────────────────

    def _build_detail_view(self) -> ft.Column:
        """Vista completa de una unidad: introducción, diagrama, desafío y quiz."""
        protocol_color = DesignTokens.get_protocol_color(self.protocol)
        unit           = self.selected_unit

        return ft.Column(
            [
                # Cabecera de detalle
                ft.Row(
                    [
                        ft.IconButton(
                            ft.Icons.ARROW_BACK_ROUNDED,
                            icon_color=protocol_color,
                            on_click=lambda _: self._back_to_list(),
                            tooltip="Volver al mapa",
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    unit["title"].upper(),
                                    size=24,
                                    weight="bold",
                                    color=DesignTokens.get_text_main(self.protocol),
                                    font_family="Lexend",
                                ),
                                ft.ProgressBar(
                                    value=0.4,
                                    color=protocol_color,
                                    bgcolor=ft.Colors.with_opacity(0.1, protocol_color),
                                    height=4,
                                    width=300,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Switch(
                            label="Modo enfoque",
                            on_change=self._toggle_immersive,
                            active_color=protocol_color,
                        ),
                    ]
                ),
                ft.Divider(height=10, color="transparent"),

                # Secciones desplazables - CENTRADAS
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    self._section("Misión",              unit["intro"],      ft.Icons.LIGHTBULB_ROUNDED),
                                    self._build_architecture_section(unit),
                                    self._build_fact_box(unit),
                                    self._section("Buenas prácticas",    unit["security"],   ft.Icons.GPP_GOOD_ROUNDED),
                                    self._build_challenge_section(unit),
                                    self._build_quiz(unit),
                                ],
                                spacing=15,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            width=800, # Limitar ancho para lectura profesional
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _section(self, title: str, text: str, icon) -> ft.Container:
        """Sección genérica de contenido con icono, título y texto."""
        protocol_color = DesignTokens.get_protocol_color(self.protocol)
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(icon, color=protocol_color, size=18),
                            ft.Text(
                                title,
                                size=14,
                                weight="bold",
                                color=protocol_color,
                                font_family="JetBrains Mono",
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Text(
                        text,
                        size=14,
                        color=DesignTokens.get_text_main(self.protocol),
                        text_align=ft.TextAlign.JUSTIFY,
                    ),
                ]
            ),
            padding=16,
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, protocol_color)),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.04, protocol_color),
        )

    def _build_architecture_section(self, unit: dict) -> ft.Container:
        """Sección 02 — estructura técnica con diagrama interactivo."""
        protocol_color = DesignTokens.get_protocol_color(self.protocol)
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.ACCOUNT_TREE_ROUNDED, color=protocol_color, size=18),
                            ft.Text(
                                "Estructura",
                                size=14,
                                weight="bold",
                                color=protocol_color,
                                font_family="JetBrains Mono",
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Text(
                        unit.get("architecture", ""),
                        size=14,
                        color=DesignTokens.get_text_main(self.protocol),
                        text_align=ft.TextAlign.JUSTIFY,
                    ),
                    ft.Container(height=15),
                    TechnicalDiagram(unit_id=unit["id"], protocol=self.protocol),
                ]
            ),
            padding=16,
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, protocol_color)),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.04, protocol_color),
        )

    def _build_fact_box(self, unit: dict) -> ft.Container:
        """Caja de dato curioso con estilo de alerta informativa."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        ft.Icons.INFO_OUTLINE_ROUNDED,
                        color=DesignTokens.COLORS["warning"],
                        size=20,
                    ),
                    ft.VerticalDivider(width=10, color="transparent"),
                    ft.Column(
                        [
                            ft.Text(
                                "¿SABÍAS QUE...?",
                                size=10,
                                weight="bold",
                                color=DesignTokens.COLORS["warning"],
                            ),
                            ft.Text(
                                unit.get("fact", ""),
                                size=13,
                                color=DesignTokens.get_text_main(self.protocol),
                                italic=True,
                            ),
                        ],
                        expand=True,
                    ),
                ]
            ),
            padding=12,
            bgcolor=ft.Colors.with_opacity(0.04, DesignTokens.COLORS["warning"]),
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, DesignTokens.COLORS["warning"])),
            border_radius=8,
        )

    def _build_challenge_section(self, unit: dict) -> ft.Container:
        """Bloque de desafío con campo de respuesta y botón de guardado."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.AUTO_AWESOME_ROUNDED,
                                color=DesignTokens.COLORS["accent"],
                                size=24,
                            ),
                            ft.Text(
                                "Desafío del sector",
                                size=18,
                                weight="bold",
                                color=DesignTokens.COLORS["accent"],
                                font_family="Lexend",
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Text(
                        unit.get("challenge", ""),
                        size=15,
                        color=DesignTokens.get_text_main(self.protocol),
                    ),
                    ft.Container(height=15),
                    self.challenge_input,
                    ft.Container(height=15),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                content=ft.Text("Guardar respuesta", weight="bold"),
                                icon=ft.Icons.CLOUD_DONE_ROUNDED,
                                on_click=lambda _: self._save_challenge(unit),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    bgcolor=DesignTokens.COLORS["accent"],
                                    padding=20,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                            ),
                            ft.TextButton(
                                "Ayuda del Maestro",
                                icon=ft.Icons.HELP_OUTLINE_ROUNDED,
                                style=ft.ButtonStyle(
                                    color=DesignTokens.get_text_dim(self.protocol)
                                ),
                            ),
                        ],
                        spacing=15,
                    ),
                ]
            ),
            padding=16,
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, DesignTokens.COLORS["accent"])),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.04, DesignTokens.COLORS["accent"]),
        )

    def _build_quiz(self, unit: dict) -> ft.Container:
        """Bloque de auto-evaluación interactiva con feedback instantáneo."""
        if "quiz" not in unit:
            return ft.Container()

        questions     = unit["quiz"]
        protocol_color = DesignTokens.get_protocol_color(self.protocol)
        quiz_controls = []

        for q_data in questions:
            options = [
                ft.ElevatedButton(
                    opt,
                    on_click=lambda e, idx=i, correct=q_data["c"]: self._check_answer(e, idx, correct),
                    style=ft.ButtonStyle(
                        color=DesignTokens.get_text_main(self.protocol),
                        bgcolor=ft.Colors.with_opacity(0.05, protocol_color),
                        padding=15,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                )
                for i, opt in enumerate(q_data["a"])
            ]
            quiz_controls.append(
                ft.Column(
                    [
                        ft.Text(
                            q_data["q"],
                            size=16,
                            weight="bold",
                            color=DesignTokens.get_text_main(self.protocol),
                        ),
                        ft.Container(height=10),
                        ft.Row(options, wrap=True, spacing=10),
                    ]
                )
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.QUIZ_ROUNDED,
                                color=DesignTokens.COLORS["tertiary"],
                                size=24,
                            ),
                            ft.Text(
                                "Autoevaluación rápida",
                                size=18,
                                weight="bold",
                                color=DesignTokens.COLORS["tertiary"],
                                font_family="Lexend",
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Divider(height=10, color="transparent"),
                    *quiz_controls,
                ]
            ),
            padding=16,
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, DesignTokens.COLORS["tertiary"])),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.04, DesignTokens.COLORS["tertiary"]),
        )

    # ──────────────────────────────────────────────────────────────────────────
    # LÓGICA DE INTERACCIÓN
    # ──────────────────────────────────────────────────────────────────────────

    def _check_answer(self, e: ft.ControlEvent, selected: int, correct: int) -> None:
        """Provee feedback visual inmediato al seleccionar una respuesta del quiz."""
        btn = e.control
        if selected == correct:
            btn.style = ft.ButtonStyle(
                bgcolor=DesignTokens.COLORS["accent"],
                color=ft.Colors.WHITE,
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8),
            )
            btn.content = ft.Text("✓ ¡CORRECTO!", weight="bold")
        else:
            btn.style = ft.ButtonStyle(
                bgcolor=DesignTokens.COLORS["critical"],
                color=ft.Colors.WHITE,
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=8),
            )
            btn.content = ft.Text("✗ INTENTA OTRA VEZ", weight="bold")
        btn.update()

    def _toggle_immersive(self, e: ft.ControlEvent) -> None:
        """Activa/desactiva el modo inmersivo (oculta el sidebar)."""
        self.immersive_mode = e.control.value
        if self.nav and self.nav.sidebar:
            self.nav.sidebar.visible = not self.immersive_mode
            try:
                self.nav.app_page.update()
            except Exception:
                pass
        self.update()

    def _open_unit_detail(self, unit: dict) -> None:
        """Navega a la vista de detalle de una unidad."""
        self.selected_unit             = unit
        self.current_view              = "detail"
        self.challenge_input.value     = ""
        self.initialize()
        self.update()

    def _back_to_list(self) -> None:
        """Regresa a la vista de lista de unidades."""
        self.current_view  = "list"
        self.selected_unit = None
        self.initialize()
        self.update()

    def _save_challenge(self, unit: dict) -> None:
        """
        Guarda la respuesta del desafío en la base de datos y marca la unidad como completada.
        Solo actúa si el campo de respuesta no está vacío.
        """
        if not self.challenge_input.value or not self.challenge_input.value.strip():
            return

        db.save_response(self.protocol, unit["id"], self.challenge_input.value)
        db.update_progress(self.protocol, unit["id"])
        self._back_to_list()
