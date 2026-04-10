"""
Módulo: dashboard.py
Archivo desarrollado por Yoangel Gómez
"""

import flet as ft
import asyncio
import random
import time

from base.module import BaseModule
from core.theme import DesignTokens
from core.content import ContentEngine
from components.glass_container import GlassContainer


class Dashboard(BaseModule):
    """
    Módulo Dashboard — panel principal de bienvenida, estado del sistema y telemetría.

    Adapta sus textos, iconos y colores al protocolo activo (alpha/delta/omega).
    Incluye tarjetas de telemetría con actualización asíncrona en tiempo real.
    """

    def __init__(self, navigation_manager=None, protocol: str = "alpha") -> None:
        super().__init__(navigation_manager, protocol)
        self.protocol_data  = ContentEngine.PROTOCOLS.get(protocol, ContentEngine.PROTOCOLS["alpha"])
        self.protocol_color = DesignTokens.get_protocol_color(protocol)

        # Contenido adaptado por protocolo desde ContentEngine
        data               = ContentEngine.DASHBOARD.get(protocol, ContentEngine.DASHBOARD["alpha"])
        self.title_text    = data["title"]
        self.status_labels = data["labels"]
        self.mission_desc  = data["mission"]

        # Estado de telemetría
        self.metric_controls: dict[str, ft.Text] = {}
        self._telemetry_active       = True
        self._telemetry_task_started = False

        self.initialize()

    # ──────────────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN DEL UI
    # ──────────────────────────────────────────────────────────────────────────

    def build(self) -> ft.Control:
        """Panel de estado compacto — métricas + acciones rápidas."""
        return ft.Column(
            controls=[
                self._build_header(),
                ft.Divider(height=20, color=DesignTokens.get_glass_border(self.protocol)),
                self._build_quick_actions(),
                ft.Divider(height=16, color="transparent"),
                self._build_telemetry_grid(),
                ft.Container(expand=True),
                self._build_info_bar(),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
        )

    def _build_header(self) -> ft.Row:
        """Cabecera compacta: título del módulo y estado de sesión."""
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            self.title_text,
                            size=26,  # Título más grande y fuerte
                            font_family="JetBrains Mono",
                            weight=ft.FontWeight.BOLD,
                            color=self.protocol_color,
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    width=8,
                                    height=8,
                                    bgcolor=DesignTokens.COLORS["accent"],
                                    border_radius=4,
                                ),
                                ft.Text(
                                    f"Sesión activa — Nivel {self.protocol.capitalize()}",
                                    size=10,
                                    color=DesignTokens.get_text_dim(self.protocol),
                                    font_family="JetBrains Mono",
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=2,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.SHIELD,
                                color=DesignTokens.COLORS["accent"],
                                size=14,
                            ),
                            ft.Text(
                                "AES-256",
                                size=10,
                                color=DesignTokens.get_text_main(self.protocol),
                            ),
                        ],
                        spacing=6,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border=ft.border.all(1, DesignTokens.get_glass_border(self.protocol)),
                    border_radius=20,
                ),
            ]
        )

    def _build_quick_actions(self) -> ft.Row:
        """Acciones rápidas de navegación a los módulos principales."""
        actions = [
            (ft.Icons.SCIENCE_ROUNDED,  "Laboratorio",    "lab",      DesignTokens.COLORS["secondary"]),
            (ft.Icons.SECURITY_ROUNDED, "Seguridad",      "security", DesignTokens.COLORS["warning"]),
        ]
        chips = []
        for icon, label, module_id, color in actions:
            chips.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(icon, color=color, size=16),
                            ft.Text(label, size=12, weight="w600",
                                    color=DesignTokens.get_text_main(self.protocol)),
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                    bgcolor=ft.Colors.with_opacity(0.08, color),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, color)),
                    border_radius=20,
                    ink=True,
                    on_click=lambda _, mid=module_id: self.nav.navigate_to(mid),
                )
            )
        return ft.Row(chips, spacing=20, wrap=True) # Más espacio entre acciones

    def _build_telemetry_grid(self) -> ft.Row:
        """Cuadrícula de tarjetas de telemetría en tiempo real."""
        return ft.Row(
            spacing=30, # Mucho más aire entre tarjetas de telemetría
            wrap=True,
            controls=[
                self._create_telemetry_card(label) for label in self.status_labels
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def _build_info_bar(self) -> ft.Container:
        """Barra inferior de información del sistema."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "E.E.D.A. OS v4.1",
                        size=10,
                        color=DesignTokens.get_text_dim(self.protocol),
                        font_family="JetBrains Mono",
                    ),
                    ft.Container(expand=True),
                    ft.Text(
                        f"{time.strftime('%d/%m/%Y %H:%M')}",
                        size=10,
                        color=DesignTokens.get_text_dim(self.protocol),
                        font_family="JetBrains Mono",
                    ),
                ]
            ),
            padding=10,
            border=ft.border.only(
                top=ft.BorderSide(1, DesignTokens.get_glass_border(self.protocol))
            ),
        )

    def _create_telemetry_card(self, label: str) -> GlassContainer:
        """
        Crea una tarjeta de telemetría individual con indicador de progreso.

        Args:
            label: Nombre del sensor / métrica.

        Returns:
            GlassContainer con valor numérico y barra de progreso.
        """
        val_control = ft.Text(
            "0%",
            size=32,
            font_family="JetBrains Mono",
            weight="bold",
            color=DesignTokens.get_text_main(self.protocol),
        )
        progress_bar = ft.ProgressBar(
            value=0,
            color=self.protocol_color,
            bgcolor=ft.Colors.with_opacity(0.1, self.protocol_color),
            height=6,
            border_radius=3,
        )
        # Almacenar referencia a la barra para actualizar eficientemente
        val_control.data = progress_bar
        self.metric_controls[label] = val_control

        return GlassContainer(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                label.upper(),
                                size=11,
                                color=self.protocol_color,
                                weight="bold",
                                font_family="JetBrains Mono",
                            ),
                            ft.Container(expand=True),
                            ft.Icon(
                                ft.Icons.SIGNAL_CELLULAR_ALT,
                                size=12,
                                color=self.protocol_color,
                            ),
                        ]
                    ),
                    ft.Divider(height=10, color="transparent"),
                    val_control,
                    ft.Container(height=5),
                    progress_bar,
                ],
                spacing=2,
            ),
            width=230,
            height=140,
            padding=20,
            protocol=self.protocol,
        )

    # ──────────────────────────────────────────────────────────────────────────
    # CICLO DE VIDA Y TELEMETRÍA ASÍNCRONA
    # ──────────────────────────────────────────────────────────────────────────

    def did_mount(self) -> None:
        """Inicia la tarea de telemetría cuando el control se monta en la página."""
        if not self._telemetry_task_started:
            self._telemetry_task_started = True
            self.page.run_task(self._update_telemetry_async)

    def cleanup(self) -> None:
        """Detiene la tarea de telemetría al abandonar el módulo."""
        self._telemetry_active = False

    async def _update_telemetry_async(self) -> None:
        """
        Actualiza las métricas de telemetría cada 2.5 s de forma no-bloqueante.
        Termina de forma segura cuando el módulo ya no está activo o la sesión finaliza.
        """
        await asyncio.sleep(0.8)
        while self._telemetry_active:
            try:
                if not self.page or self.page.session_id is None:
                    break

                for label, control in self.metric_controls.items():
                    val = random.randint(87, 100)
                    control.value = f"{val}%"
                    if isinstance(getattr(control, "data", None), ft.ProgressBar):
                        control.data.value = val / 100

                try:
                    self.update()
                except Exception:
                    pass

                await asyncio.sleep(2.5)

            except Exception:
                break
