"""
Módulo: technical_diagram.py  (components/)
Propósito: Diagramas técnicos interactivos por unidad pedagógica.
Política (Cot.md): Colores desde DesignTokens.get_protocol_color(). Cero valores hardcoded.
"""

import flet as ft
from core.theme import DesignTokens


class TechnicalDiagram(ft.Container):
    """
    Componente para renderizar diagramas técnicos interactivos según la unidad pedagógica.

    Cada diagrama es específico a la unidad (hardware, logic, network, etc.) y
    usa el color del protocolo activo para mantener la coherencia visual.

    Unidades soportadas: hardware, logic, network, cybersecurity, os, ai.
    """

    def __init__(self, unit_id: str, protocol: str, **kwargs) -> None:
        """
        Args:
            unit_id:  Identificador de la unidad pedagógica.
            protocol: Protocolo activo ("alpha", "delta", "omega").
            **kwargs: Parámetros adicionales para ft.Container.
        """
        super().__init__(**kwargs)
        self.unit_id        = unit_id
        self.protocol       = protocol
        self.protocol_color = DesignTokens.get_protocol_color(protocol)

        # Estilos del contenedor del diagrama (desde DesignTokens)
        self.border_radius = 8
        self.padding       = 16
        self.bgcolor       = ft.Colors.with_opacity(0.04, self.protocol_color)
        self.border        = ft.border.all(1, ft.Colors.with_opacity(0.15, self.protocol_color))
        self.animate_scale = ft.Animation(150, ft.AnimationCurve.DECELERATE)
        self.content       = self._build_diagram()

    # ──────────────────────────────────────────────────────────────────────────
    # DESPACHO DE DIAGRAMAS
    # ──────────────────────────────────────────────────────────────────────────

    def _build_diagram(self) -> ft.Control:
        """Selecciona y construye el diagrama correspondiente a la unidad."""
        diagrams = {
            "hardware":      self._hardware_diagram,
            "logic":         self._logic_diagram,
            "network":       self._network_diagram,
            "cybersecurity": self._security_diagram,
            "os":            self._os_diagram,
            "ai":            self._ai_diagram,
            "programming":   self._programming_diagram,
            "ethics":        self._ethics_diagram,
        }
        builder = diagrams.get(self.unit_id)
        if builder:
            return builder()
        return ft.Text(
            "DIAGRAMA EN PROCESO DE CARGA...",
            size=12,
            italic=True,
            color=DesignTokens.get_text_dim(self.protocol),
        )

    # ──────────────────────────────────────────────────────────────────────────
    # DIAGRAMAS POR UNIDAD
    # ──────────────────────────────────────────────────────────────────────────

    def _os_diagram(self) -> ft.Column:
        """Diagrama de capas del Sistema Operativo (Usuario → Kernel → Hardware)."""
        layers = [
            ("USUARIO",           0.12),
            ("APLICACIONES",      0.22),
            ("KERNEL (CEREBRO)",  0.42, True),
            ("HARDWARE (PIEZAS)", 0.12),
        ]
        controls = []
        for layer in layers:
            label  = layer[0]
            opacity = layer[1]
            bold   = len(layer) > 2 and layer[2]
            controls.append(self._layer_box(label, ft.Colors.with_opacity(opacity, self.protocol_color), bold=bold))
            if label != "HARDWARE (PIEZAS)":
                controls.append(
                    ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN, size=15, color=self.protocol_color)
                )
        return ft.Column(controls, horizontal_alignment="center", spacing=2)

    def _hardware_diagram(self) -> ft.Row:
        """Diagrama CPU → RAM → DISK para la unidad de Hardware."""
        return ft.Row(
            [
                self._box("CEREBRO (CPU)", ft.Icons.MEMORY,   "Procesamiento"),
                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=self.protocol_color),
                self._box("MEMORIA (RAM)", ft.Icons.SD_CARD,  "Donde trabaja"),
                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=self.protocol_color),
                self._box("BAÚL (DISK)",   ft.Icons.STORAGE,  "Donde guarda"),
            ],
            alignment="center",
            spacing=20,
        )

    def _logic_diagram(self) -> ft.Row:
        """Diagrama ENTRADA → LÓGICA → SALIDA para la unidad de Lógica."""
        return ft.Row(
            [
                self._box("ENTRADA", ft.Icons.INPUT,          "Tus datos"),
                ft.Icon(ft.Icons.SETTINGS_SUGGEST, color=self.protocol_color),
                self._box("LÓGICA",  ft.Icons.CODE,           "Instrucciones"),
                ft.Icon(ft.Icons.OUTPUT, color=self.protocol_color),
                self._box("SALIDA",  ft.Icons.AUTO_AWESOME,   "Resultado"),
            ],
            alignment="center",
            spacing=20,
        )

    def _network_diagram(self) -> ft.Column:
        """Diagrama Cliente — Internet — Servidor para la unidad de Redes."""
        return ft.Column(
            [
                ft.Row(
                    [
                        self._box("TÚ (CLIENTE)",  ft.Icons.LAPTOP,  "Pides algo"),
                        ft.Icon(ft.Icons.LANGUAGE, color=self.protocol_color, size=30),
                        self._box("NUBE (SERVER)", ft.Icons.DNS,     "Te responde"),
                    ],
                    alignment="center",
                ),
                ft.Container(height=10),
                ft.Text(
                    "CONEXIÓN SEGURA ACTIVA",
                    size=10,
                    font_family="JetBrains Mono",
                    color=DesignTokens.COLORS["accent"],
                    weight="bold",
                ),
            ],
            horizontal_alignment="center",
        )

    def _security_diagram(self) -> ft.Stack:
        """Diagrama de anillos concéntricos para la unidad de Ciberseguridad."""
        c = self.protocol_color
        return ft.Stack(
            [
                ft.Container(
                    width=190, height=190,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, c)),
                    border_radius=100,
                ),
                ft.Container(
                    width=135, height=135,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, c)),
                    border_radius=80,
                ),
                ft.Container(
                    width=80, height=80,
                    bgcolor=ft.Colors.with_opacity(0.08, c),
                    border_radius=50,
                    content=ft.Icon(ft.Icons.LOCK, color=c, size=32),
                ),
            ],
            alignment=ft.Alignment(0, 0),
        )

    def _ai_diagram(self) -> ft.Row:
        """Diagrama de red neuronal simplificada para la unidad de IA."""
        c = self.protocol_color
        return ft.Row(
            [
                ft.Column(
                    [ft.CircleAvatar(radius=7, bgcolor=c) for _ in range(3)],
                    spacing=14,
                ),
                ft.Icon(ft.Icons.GRAIN, color=c, size=35),
                ft.Column(
                    [ft.CircleAvatar(radius=7, bgcolor=c) for _ in range(4)],
                    spacing=14,
                ),
                ft.Icon(ft.Icons.GRAIN, color=c, size=35),
                ft.Column(
                    [ft.CircleAvatar(radius=7, bgcolor=c) for _ in range(2)],
                    spacing=14,
                ),
            ],
            alignment="center",
            spacing=20,
        )

    def _programming_diagram(self) -> ft.Row:
        """Diagrama IDEA → CÓDIGO → PROGRAMA para la unidad de Programación."""
        return ft.Row(
            [
                self._box("IDEA",     ft.Icons.LIGHTBULB_OUTLINE, "Tu concepto"),
                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=self.protocol_color),
                self._box("CÓDIGO",   ft.Icons.CODE,              "Instrucciones"),
                ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, color=self.protocol_color),
                self._box("PROGRAMA", ft.Icons.APPS,              "Resultado final"),
            ],
            alignment="center",
            spacing=20,
        )

    def _ethics_diagram(self) -> ft.Column:
        """Diagrama de relación Usuario ↔ Reglas ↔ Comunidad para la unidad de Ética."""
        c = self.protocol_color
        return ft.Column(
            [
                ft.Row(
                    [
                        self._box("USUARIO",   ft.Icons.PERSON,  "Tus acciones"),
                        ft.Icon(ft.Icons.SWAP_HORIZ_ROUNDED, color=c, size=30),
                        self._box("REGLAS",    ft.Icons.GAVEL,   "Ética digital"),
                        ft.Icon(ft.Icons.SWAP_HORIZ_ROUNDED, color=c, size=30),
                        self._box("COMUNIDAD", ft.Icons.GROUPS,  "Impacto social"),
                    ],
                    alignment="center",
                ),
                ft.Container(height=10),
                ft.Text(
                    "TUS ACCIONES IMPACTAN A LA COMUNIDAD",
                    size=10,
                    font_family="JetBrains Mono",
                    color=DesignTokens.COLORS["accent"],
                    weight="bold",
                ),
            ],
            horizontal_alignment="center",
        )

    # ──────────────────────────────────────────────────────────────────────────
    # HELPERS DE CONSTRUCCIÓN
    # ──────────────────────────────────────────────────────────────────────────

    def _box(self, label: str, icon, subtitle: str) -> ft.Container:
        """Nodo de diagrama cuadrado con icono, etiqueta y subtítulo."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, color=self.protocol_color, size=28),
                    ft.Text(
                        label,
                        weight="bold",
                        size=12,
                        color=DesignTokens.get_text_main(self.protocol),
                    ),
                    ft.Text(
                        subtitle,
                        size=9,
                        color=DesignTokens.get_text_dim(self.protocol),
                    ),
                ],
                horizontal_alignment="center",
                spacing=2,
            ),
            width=120,
            padding=10,
            bgcolor=ft.Colors.with_opacity(0.04, self.protocol_color),
            border=ft.border.all(1, ft.Colors.with_opacity(0.15, self.protocol_color)),
            border_radius=8,
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=self._on_hover_box,
        )

    def _layer_box(self, text: str, bgcolor, bold: bool = False) -> ft.Container:
        """Caja de capa para el diagrama de SO."""
        return ft.Container(
            content=ft.Text(
                text,
                weight="bold" if bold else "normal",
                size=11,
                color=DesignTokens.get_text_main(self.protocol),
            ),
            bgcolor=bgcolor,
            padding=10,
            border_radius=8,
            alignment=ft.Alignment(0, 0),
            width=260,
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
            on_hover=self._on_hover_box,
        )

    def _on_hover_box(self, e: ft.HoverEvent) -> None:
        """Efecto de escala y cambio de fondo al hacer hover sobre nodos del diagrama."""
        is_hovered = e.data == "true"
        e.control.scale  = 1.06 if is_hovered else 1.0
        e.control.bgcolor = (
            ft.Colors.with_opacity(0.08, self.protocol_color)
            if is_hovered
            else ft.Colors.with_opacity(0.04, self.protocol_color)
        )
        e.control.update()
