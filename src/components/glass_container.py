"""
Módulo: glass_container.py
Archivo desarrollado por Yoangel Gómez
"""

import flet as ft
from core.theme import DesignTokens


class GlassContainer(ft.Container):
    """
    Contenedor con estilo Glassmorphism que se adapta al protocolo activo (Alpha/Delta/Omega).

    Combina:
        - Fondo semitransparente basado en el color del protocolo.
        - Borde sutil para la ilusión de profundidad.
        - Sombra suave para elevar el elemento visualmente.
        - Gradiente blanco para simular el reflejo del vidrio.

    Uso:
        GlassContainer(
            content=ft.Text("Hola"),
            protocol="delta",
            padding=20
        )
    """

    def __init__(
        self,
        content: ft.Control | None = None,
        padding: ft.Padding | int | None = None,
        margin: ft.Margin | int | None = None,
        protocol: str = "alpha",
        **kwargs,
    ) -> None:
        """
        Args:
            content:  Control hijo a mostrar dentro del contenedor.
            padding:  Relleno interno. Por defecto usa get_spacing(1) de DesignTokens.
            margin:   Margen externo. Por defecto 0.
            protocol: Protocolo activo para derivar los colores ("alpha", "delta", "omega").
            **kwargs: Parámetros adicionales que sobreescribirán los estilos default.
        """
        tokens = DesignTokens

        # Estilo base Glassmorphism - Más sólido y definido (15% de opacidad)
        glass_defaults: dict = {
            "blur":           ft.Blur(15, 15, ft.BlurTileMode.MIRROR),
            "animate_opacity": 200,
            "border_radius":  20,
            "border":         ft.border.all(1.5, ft.Colors.with_opacity(0.18, ft.Colors.ON_SURFACE)),
            "bgcolor":        ft.Colors.with_opacity(0.15, ft.Colors.ON_SURFACE),
            "shadow":         ft.BoxShadow(
                                  spread_radius=1,
                                  blur_radius=12,  # Sombras más cortas y definidas
                                  color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                                  offset=ft.Offset(0, 4),
                              ),
            "padding": padding if padding is not None else tokens.get_spacing(1),
            "margin":  margin  if margin  is not None else 0,
        }
        # kwargs explícitos sobreescriben los defaults (permite personalización puntual)
        glass_defaults.update(kwargs)

        super().__init__(content=content, **glass_defaults)
