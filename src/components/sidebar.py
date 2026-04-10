"""
Módulo: sidebar.py
Archivo desarrollado por Yoangel Gómez
"""

import flet as ft
from core.theme import DesignTokens
from core.content import ContentEngine

# Definición de ítems de navegación por protocolo
# (icon, label_display, module_id)
_NAV_ITEMS: dict[str, list[tuple]] = {
    "alpha": [
        (ft.Icons.MAP_ROUNDED,              "Explorar Temas",        "zones"),
        (ft.Icons.BRUSH_ROUNDED,            "Taller Creativo",       "lab"),
        (ft.Icons.SHIELD_ROUNDED,           "Panel de Control",      "security"),
        (ft.Icons.BAR_CHART_ROUNDED,        "Resumen",               "dashboard"),
    ],
    "delta": [
        (ft.Icons.AUTO_STORIES_ROUNDED,     "Temas",                 "zones"),
        (ft.Icons.SCIENCE_ROUNDED,          "Laboratorio",           "lab"),
        (ft.Icons.DASHBOARD_ROUNDED,        "Panel de Control",      "security"),
        (ft.Icons.BAR_CHART_ROUNDED,        "Panel",                 "dashboard"),
    ],
    "omega": [
        (ft.Icons.ACCOUNT_TREE_ROUNDED,     "Topología de Red",      "zones"),
        (ft.Icons.TERMINAL_ROUNDED,         "Simulador",             "lab"),
        (ft.Icons.DASHBOARD_ROUNDED,        "Puente de Mando",       "security"),
        (ft.Icons.BAR_CHART_ROUNDED,        "Dashboard",             "dashboard"),
    ],
}


class Sidebar(ft.Container):
    """
    Barra de navegación lateral para E.E.D.A.

    Se adapta visualmente y semánticamente según el protocolo activo:
        - Alpha  → Narrativa espacial / Exploradores / Verde
        - Delta  → Terminales / Operadores / Azul
        - Omega  → Arquitectura / Hackers / Rojo-Naranja

    Política:
        - Colores siempre desde DesignTokens.get_protocol_color().
        - Labels siempre desde _NAV_ITEMS (nunca hardcoded en el método).
        - set_active() actualiza el estado sin reconstruir el árbol completo.
    """

    def __init__(self, on_nav_change, on_home=None, protocol: str = "alpha") -> None:
        """
        Args:
            on_nav_change: Callback que recibe el module_id seleccionado.
            on_home:       Callback para retornar a la selección de nivel.
            protocol:      Protocolo activo del usuario.
        """
        super().__init__()
        self.on_nav_change  = on_nav_change
        self.on_home        = on_home
        self.protocol        = protocol
        self.active_module   = "zones"

        self.protocol_data  = ContentEngine.PROTOCOLS.get(protocol, ContentEngine.PROTOCOLS["alpha"])
        self.protocol_color = DesignTokens.get_protocol_color(protocol)

        # Dimensiones y estilos del contenedor (desde DesignTokens)
        self.width   = 220
        self.bgcolor = ft.Colors.with_opacity(0.06, self.protocol_color)
        self.padding = ft.padding.symmetric(horizontal=14, vertical=20)
        self.border  = ft.border.only(
            right=ft.BorderSide(1, DesignTokens.get_glass_border(self.protocol))
        )

        self.nav_items_container = ft.Column(spacing=8)
        self._build_sidebar()

    # ──────────────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN
    # ──────────────────────────────────────────────────────────────────────────

    def _build_sidebar(self) -> None:
        """Construye el contenido completo del sidebar."""
        nav_labels = _NAV_ITEMS.get(self.protocol, _NAV_ITEMS["alpha"])

        self.nav_items: dict[str, ft.Container] = {}
        controls = []
        for icon, title, module_id in nav_labels:
            item = self._build_nav_item(icon, title, module_id)
            self.nav_items[module_id] = item
            controls.append(item)

        self.nav_items_container.controls = controls
        self.set_active(self.active_module)  # Aplicar estado inicial

        self.content = ft.Column(
            controls=[
                self._build_header(),
                ft.Container(height=8),
                self.nav_items_container,
                ft.Container(expand=True),
                self._build_footer(),
            ],
            expand=True,
        )

    def _build_header(self) -> ft.Container:
        """Cabecera compacta del sidebar."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        width=3,
                        height=20,
                        bgcolor=self.protocol_color,
                        border_radius=2,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                f"E.E.D.A. — {self.protocol.capitalize()}",
                                size=16,
                                weight="bold",
                                color=DesignTokens.get_text_main(self.protocol),
                            ),
                            ft.Text(
                                self.protocol_data["age_range"],
                                size=9,
                                color=DesignTokens.get_text_dim(self.protocol),
                                font_family="JetBrains Mono",
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=8,
            ),
            margin=ft.margin.only(bottom=16, top=4),
        )

    def _build_footer(self) -> ft.Container:
        """Pie minimalista del sidebar: solo marca de agua o estado."""
        
        # Eliminados los botones de tema (movidos a settings en main.py)
        theme_buttons = ft.Container()  # Espacio vacío o removido


        return ft.Container(
            content=ft.Column(
                [
                    ft.Divider(height=10, color="transparent"),
                    theme_buttons,
                    ft.Divider(height=10, color="transparent"),
                    ft.ElevatedButton(
                        "Cambiar Nivel",
                        icon=ft.Icons.REPLAY_ROUNDED,
                        on_click=lambda _: self.on_home() if self.on_home else None,
                        bgcolor=ft.Colors.with_opacity(0.1, DesignTokens.COLORS["accent"]),
                        color=DesignTokens.get_text_main(self.protocol),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=15
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            padding=ft.padding.only(bottom=10, top=10),
        )

    def _build_nav_item(self, icon, title: str, module_id: str) -> ft.Container:
        """Construye un ítem de navegación individual."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color=DesignTokens.get_text_dim(self.protocol), size=20),
                    ft.Text(
                        title,
                        color=DesignTokens.get_text_dim(self.protocol),
                        size=13,
                        weight="w600",
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=12),
            on_click=lambda _, mid=module_id: self.on_nav_change(mid),
            border_radius=10,
            ink=True,
            on_hover=lambda e, mid=module_id: self._handle_hover(e, mid),
        )

    # ──────────────────────────────────────────────────────────────────────────
    # ESTADO ACTIVO
    # ──────────────────────────────────────────────────────────────────────────

    def set_active(self, module_id: str) -> None:
        """
        Actualiza el ítem activo en el sidebar con efecto visual premium.
        Usa gradiente lateral y borde izquierdo de acento.

        Args:
            module_id: Identificador del módulo que debe marcarse como activo.
        """
        self.active_module = module_id

        for mid, item in self.nav_items.items():
            is_active = mid == module_id

            if is_active:
                item.bgcolor  = None
                item.gradient = DesignTokens.get_active_nav_gradient(self.protocol)
                item.border   = ft.Border(left=ft.BorderSide(3, self.protocol_color))
            else:
                item.bgcolor  = None
                item.gradient = None
                item.border   = None

            # Actualizar color del icono y texto
            row: ft.Row = item.content
            row.controls[0].color = (
                self.protocol_color if is_active else DesignTokens.get_text_dim(self.protocol)
            )
            row.controls[1].color = (
                DesignTokens.get_text_main(self.protocol)
                if is_active
                else DesignTokens.get_text_dim(self.protocol)
            )

            try:
                item.update()
            except Exception:
                pass

        try:
            self.update()
        except Exception:
            pass

    # ──────────────────────────────────────────────────────────────────────────
    # EVENTOS
    # ──────────────────────────────────────────────────────────────────────────

    def _handle_hover(self, e: ft.HoverEvent, module_id: str) -> None:
        """Efecto hover sobre ítems inactivos."""
        if module_id == self.active_module:
            return
        e.control.bgcolor = (
            ft.Colors.with_opacity(0.08, self.protocol_color)
            if e.data == "true"
            else None
        )
        e.control.update()
