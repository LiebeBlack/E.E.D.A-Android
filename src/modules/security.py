"""
Módulo: security.py
Archivo desarrollado por Yoangel Gómez
"""

import flet as ft

from base.module import BaseModule
from core.theme import DesignTokens
from core.content import ContentEngine
from components.glass_container import GlassContainer


class Security(BaseModule):
    """
    Módulo Security — Panel de ciberseguridad adaptativo por protocolo.

    Contiene:
        - Cuadrícula de métricas de estado del sistema.
        - Lista de buenas prácticas filtradas por protocolo.
        - Simulador de terminal con comandos educativos.
    """

    def __init__(self, navigation_manager=None, protocol: str = "alpha") -> None:
        super().__init__(navigation_manager, protocol)
        self.protocol_color = DesignTokens.get_protocol_color(protocol)

        data              = ContentEngine.SECURITY_METRICS.get(protocol, ContentEngine.SECURITY_METRICS["alpha"])
        self.title_text   = data["title"]
        self.metrics_raw  = data["metrics"]

        # Referencia al texto de salida del terminal (se asigna en _build_terminal)
        self.term_output: ft.Text | None = None

        self.initialize()

    # ──────────────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN
    # ──────────────────────────────────────────────────────────────────────────

    def build(self) -> ft.Control:
        """Panel de ciberdefensa: terminal como herramienta principal."""
        return ft.Column(
            controls=[
                self._build_header(),
                ft.Divider(height=14, color=DesignTokens.get_glass_border(self.protocol)),
                # Sección principal: terminal + prácticas lado a lado
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.TERMINAL_ROUNDED,
                                                color=self.protocol_color, size=16),
                                        ft.Text(
                                            "Terminal de comandos",
                                            size=13,
                                            weight="bold",
                                            color=self.protocol_color,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                ft.Container(height=8),
                                self._build_terminal_simulator(),
                            ],
                            expand=True,
                        ),
                        ft.VerticalDivider(width=24, color=DesignTokens.get_glass_border(self.protocol)),
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.GPP_MAYBE,
                                                color=DesignTokens.COLORS["warning"], size=16),
                                        ft.Text(
                                            "Buenas prácticas",
                                            size=13,
                                            weight="bold",
                                            color=DesignTokens.get_text_main(self.protocol),
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                ft.Container(height=8),
                                self._build_best_practices(),
                            ],
                            expand=True,
                        ),
                    ],
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=0,
                ),
                ft.Divider(height=16, color=DesignTokens.get_glass_border(self.protocol)),
                # Métricas como fila compacta en la parte inferior
                ft.Row(
                    [
                        ft.Icon(ft.Icons.MONITOR_HEART, color=self.protocol_color, size=14),
                        ft.Text(
                            "Métricas del sistema",
                            size=12,
                            weight="bold",
                            color=DesignTokens.get_text_dim(self.protocol),
                        ),
                    ],
                    spacing=8,
                ),
                ft.Container(height=8),
                self._build_metrics_row(),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def _build_header(self) -> ft.Row:
        """Cabecera compacta del panel de seguridad."""
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            self.title_text,
                            size=20,
                            font_family="JetBrains Mono",
                            weight=ft.FontWeight.BOLD,
                            color=self.protocol_color,
                        ),
                        ft.Text(
                            "Estado del sistema: Seguro",
                            size=10,
                            color=DesignTokens.get_text_dim(self.protocol),
                            font_family="JetBrains Mono",
                        ),
                    ],
                    spacing=2,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(width=8, height=8,
                                         bgcolor=DesignTokens.COLORS["accent"],
                                         border_radius=4),
                            ft.Text("En línea", size=10,
                                    color=DesignTokens.COLORS["accent"],
                                    weight="bold"),
                        ],
                        spacing=6,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.3, DesignTokens.COLORS["accent"])),
                    border_radius=20,
                ),
            ]
        )

    def _build_metrics_grid(self) -> ft.Row:
        """Cuadrícula de tarjetas de métricas de seguridad."""
        return ft.Row(
            wrap=True,
            spacing=20,
            controls=[self._create_metric_card(m) for m in self.metrics_raw],
        )

    def _build_metrics_row(self) -> ft.Row:
        """Fila compacta de métricas — chips con valor, para mostrar en pie del panel."""
        chips = []
        for metric in self.metrics_raw:
            icon  = getattr(ft.Icons, metric.get("icon_name", "SHIELD_ROUNDED"), ft.Icons.SHIELD_ROUNDED)
            color = DesignTokens.COLORS.get(metric.get("color_key", "primary"), self.protocol_color)
            chips.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(icon, size=14, color=color),
                            ft.Text(
                                metric.get("label", "").upper(),
                                size=10,
                                color=DesignTokens.get_text_dim(self.protocol),
                                font_family="JetBrains Mono",
                            ),
                            ft.Text(
                                metric.get("value", ""),
                                size=12,
                                weight="bold",
                                color=DesignTokens.get_text_main(self.protocol),
                            ),
                        ],
                        spacing=6,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=7),
                    bgcolor=ft.Colors.with_opacity(0.06, color),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.15, color)),
                    border_radius=20,
                )
            )
        return ft.Row(chips, spacing=10, wrap=True)

    def _create_metric_card(self, metric: dict) -> GlassContainer:
        """Tarjeta individual de métrica de seguridad."""
        icon  = getattr(ft.Icons, metric.get("icon_name", "SHIELD_ROUNDED"), ft.Icons.SHIELD_ROUNDED)
        color = DesignTokens.COLORS.get(metric.get("color_key", "primary"), self.protocol_color)

        return GlassContainer(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=30),
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(0.1, color),
                        border_radius=10,
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Text(
                        metric.get("label", "").upper(),
                        size=11,
                        color=DesignTokens.get_text_dim(self.protocol),
                        font_family="JetBrains Mono",
                        weight="bold",
                    ),
                    ft.Text(
                        metric.get("value", ""),
                        size=22,
                        weight="bold",
                        color=DesignTokens.get_text_main(self.protocol),
                    ),
                ],
                spacing=2,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=230,
            height=160,
            protocol=self.protocol,
            padding=20,
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.2, color)),
        )

    def _build_best_practices(self) -> ft.Column:
        """Lista de buenas prácticas adaptada al protocolo activo."""
        practices = ContentEngine.SECURITY_PRACTICES.get(
            self.protocol, ContentEngine.SECURITY_PRACTICES["alpha"]
        )

        controls = []
        for text, icon_name in practices:
            icon = getattr(ft.Icons, icon_name, ft.Icons.SHIELD_ROUNDED)
            controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(icon, color=self.protocol_color, size=24),
                            ft.Text(
                                text,
                                size=14,
                                color=DesignTokens.get_text_main(self.protocol),
                                weight="w500",
                                expand=True,
                            ),
                        ],
                        spacing=15,
                    ),
                    padding=15,
                    bgcolor=ft.Colors.with_opacity(0.04, self.protocol_color),
                    border_radius=12,
                    border=ft.border.all(
                        1, ft.Colors.with_opacity(0.15, self.protocol_color)
                    ),
                )
            )

        return ft.Column(controls, spacing=10)

    def _build_terminal_simulator(self) -> ft.Container:
        """
        Simulador de terminal con comandos educativos predefinidos.
        Enseña el concepto de auditoría y estado del firewall de forma interactiva.
        """
        self.term_output = ft.Text(
            "Listo para recibir comandos.",
            font_family="JetBrains Mono",
            size=11,
            color=DesignTokens.get_text_main(self.protocol),
        )

        # Respuestas simuladas por comando
        _CMD_LOG: dict[str, list[str]] = {
            "audit": [
                "> Iniciando auditoría de procesos...",
                "> Verificando privilegios de usuario...",
                "> Sin anomalías detectadas.",
            ],
            "firewall": [
                "> Consultando firewall...",
                "> Puertos activos: 80, 443, 22",
                "> Perímetro activo y seguro.",
            ],
            "clear": [""],
        }

        def run_cmd(cmd: str) -> None:
            if cmd == "clear":
                self.term_output.value = ""
            else:
                lines = _CMD_LOG.get(cmd, [f"> Error: Comando '{cmd}' no reconocido."])
                # Ahora agregamos al historial en lugar de reemplazar
                new_text = "\n".join(lines)
                if self.term_output.value:
                    self.term_output.value += f"\n\n{new_text}"
                else:
                    self.term_output.value = new_text
            self.update()

        # Color del fondo del terminal: negro puro para Omega (tema hacker)
        terminal_bg = (
            "#0D0D0D"
            if self.protocol == "omega"
            else ft.Colors.with_opacity(0.1, self.protocol_color)
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column([self.term_output], scroll=ft.ScrollMode.AUTO, expand=True), # Permitir scroll
                        padding=15,
                        bgcolor=terminal_bg,
                        border_radius=10,
                        height=200, # Un poco más alto para ver el historial
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "AUDIT_KERN",
                                on_click=lambda _: run_cmd("audit"),
                                bgcolor=ft.Colors.with_opacity(0.1, self.protocol_color),
                                color=self.protocol_color,
                            ),
                            ft.ElevatedButton(
                                "FW_STATUS",
                                on_click=lambda _: run_cmd("firewall"),
                                bgcolor=ft.Colors.with_opacity(0.1, self.protocol_color),
                                color=self.protocol_color,
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_SWEEP_ROUNDED,
                                on_click=lambda _: run_cmd("clear"),
                                icon_color=DesignTokens.get_text_dim(self.protocol),
                                tooltip="Limpiar terminal",
                            ),
                        ],
                        spacing=10,
                    ),
                ]
            ),
            padding=20,
            bgcolor=ft.Colors.with_opacity(0.05, self.protocol_color),
            border_radius=15,
            border=ft.border.all(1, DesignTokens.get_glass_border(self.protocol)),
        )
