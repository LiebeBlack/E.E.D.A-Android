"""
Módulo: module.py  (base/module.py)
Propósito: Clase base abstracta para todos los módulos de E.E.D.A.
Política (Cot.md): Toda nueva pantalla/módulo principal debe heredar de BaseModule.
"""

import flet as ft
from abc import ABC, abstractmethod
from core.theme import DesignTokens


class BaseModule(ft.Container, ABC):
    """
    Clase base para todos los módulos principales de E.E.D.A.

    Características:
        - Hereda de ft.Container para poder insertarse directamente en el layout.
        - Expone el método abstracto `build()` que cada módulo debe implementar.
        - Provee `initialize()` para separar la configuración del contenido.
        - Provee `cleanup()` para liberar recursos antes de ser destruido.

    Uso:
        class MiModulo(BaseModule):
            def build(self) -> ft.Control:
                return ft.Text("Hola!")
    """

    def __init__(
        self,
        navigation_manager=None,
        protocol: str = "alpha",
        **kwargs,
    ) -> None:
        """
        Args:
            navigation_manager: Referencia a la App principal para navegar entre módulos.
            protocol: Protocolo activo ("alpha", "delta", "omega").
            **kwargs: Parámetros adicionales pasados a ft.Container.
        """
        super().__init__(**kwargs)
        self.nav = navigation_manager
        self.protocol = protocol
        self.expand = True

        # Configuración base de glassmorphism derivada de DesignTokens
        self.glass_config: dict = {
            "blur":          DesignTokens.GLASS_STYLE["blur"],
            "opacity":       DesignTokens.GLASS_STYLE["opacity"],
            "border_radius": DesignTokens.GLASS_STYLE["border_radius"],
            "border":        ft.border.all(1, DesignTokens.get_glass_border(self.protocol)),
            "bgcolor":       DesignTokens.get_glass_bg(self.protocol),
        }

    # ──────────────────────────────────────────────────────────────────────────
    # INTERFAZ ABSTRACTA
    # ──────────────────────────────────────────────────────────────────────────

    @abstractmethod
    def build(self) -> ft.Control:
        """
        Construye y retorna el árbol de controles principal del módulo.
        Debe ser implementado por cada subclase.
        """
        ...

    # ──────────────────────────────────────────────────────────────────────────
    # CICLO DE VIDA
    # ──────────────────────────────────────────────────────────────────────────

    def initialize(self) -> None:
        """
        Inicializa o reinicializa el contenido del módulo llamando a `build()`.
        Se invoca después de que el constructor del hijo ha configurado sus datos.
        """
        self.content = self.build()

    def cleanup(self) -> None:
        """
        Libera recursos antes de que el módulo sea destruido o reemplazado.
        Sobrescribir en módulos que gestionen tareas async o suscripciones al bus.
        """
        pass
