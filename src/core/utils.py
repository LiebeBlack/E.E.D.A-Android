"""
Módulo: utils.py
Propósito: Funciones utilitarias reutilizables para toda la aplicación.
"""

from typing import Any, Callable, TypeVar
import asyncio
import logging
import flet as ft


logger = logging.getLogger(__name__)
T = TypeVar('T')


def safe_update(control: ft.Control | None) -> None:
    """
    Actualiza un control de forma segura, manejando excepciones.
    
    Args:
        control: Control Flet a actualizar.
    """
    if control is None:
        return
    try:
        control.update()
    except Exception as e:
        logger.debug(f"Error actualizando control: {e}")


def safe_page_update(page: ft.Page | None) -> None:
    """
    Actualiza una página de forma segura, manejando excepciones.
    
    Args:
        page: Página Flet a actualizar.
    """
    if page is None:
        return
    try:
        page.update()
    except Exception as e:
        logger.debug(f"Error actualizando página: {e}")


def close_all_overlays(page: ft.Page | None) -> None:
    """
    Cierra todos los overlays abiertos en una página.
    
    Args:
        page: Página Flet con overlays.
    """
    if page is None:
        return
    try:
        for overlay in list(page.overlay):
            try:
                page.close(overlay)
            except Exception:
                pass
    except Exception as e:
        logger.debug(f"Error cerrando overlays: {e}")


def get_icon_by_name(icon_name: str, default: str = "HELP") -> str:
    """
    Obtiene un icono de Flet por nombre de forma segura.
    
    Args:
        icon_name: Nombre del icono.
        default: Nombre del icono por defecto si no se encuentra.
        
    Returns:
        Icono de Flet.
    """
    return getattr(ft.Icons, icon_name, getattr(ft.Icons, default, ft.Icons.HELP))


def format_system_info(items: dict[str, Any]) -> str:
    """
    Formatea información del sistema como texto.
    
    Args:
        items: Diccionario con información del sistema.
        
    Returns:
        Texto formateado.
    """
    lines = ["=== EVENT BUS STATE ==="]
    if items:
        for key, value in items.items():
            lines.append(f"  [{key}] → {value}")
    else:
        lines.append("  (vacío — sin suscripciones activas)")
    return "\n".join(lines)


async def sleep_safe(seconds: float) -> None:
    """
    Espera de forma segura, manejando excepciones.
    
    Args:
        seconds: Segundos a esperar.
    """
    try:
        await asyncio.sleep(seconds)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.debug(f"Error en sleep: {e}")


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Restringe un valor dentro de un rango.
    
    Args:
        value: Valor a restringir.
        min_val: Valor mínimo.
        max_val: Valor máximo.
        
    Returns:
        Valor restringido.
    """
    return max(min_val, min(max_val, value))


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Trunca un texto si excede la longitud máxima.
    
    Args:
        text: Texto a truncar.
        max_length: Longitud máxima.
        suffix: Sufijo a agregar si se trunca.
        
    Returns:
        Texto truncado.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


class Debouncer:
    """
    Debouncer para limitar la frecuencia de llamadas a una función.
    """
    
    def __init__(self, delay: float = 0.3):
        self.delay = delay
        self._task: asyncio.Task | None = None
    
    async def _run(self, func: Callable[..., T], *args, **kwargs) -> T:
        await asyncio.sleep(self.delay)
        return func(*args, **kwargs)
    
    def call(self, func: Callable[..., T], *args, **kwargs) -> None:
        """Llama a la función después del delay, cancelando llamadas previas."""
        if self._task and not self._task.done():
            self._task.cancel()
        self._task = asyncio.create_task(self._run(func, *args, **kwargs))


class CachedProperty:
    """
    Decorador para propiedades cacheadas (similar a functools.cached_property).
    """
    
    def __init__(self, func: Callable[..., T]):
        self.func = func
        self.name = func.__name__
        self._cache: dict[int, T] = {}
    
    def __get__(self, instance: Any, owner: type) -> T:
        if instance is None:
            return self
        
        instance_id = id(instance)
        if instance_id not in self._cache:
            self._cache[instance_id] = self.func(instance)
        return self._cache[instance_id]
    
    def __delete__(self, instance: Any) -> None:
        instance_id = id(instance)
        self._cache.pop(instance_id, None)


def batch_updates(page: ft.Page, controls: list[ft.Control]) -> None:
    """
    Actualiza múltiples controles en batch para mejor rendimiento.
    
    Args:
        page: Página Flet.
        controls: Lista de controles a actualizar.
    """
    if page is None:
        return
    
    try:
        for control in controls:
            if control:
                control.update()
        page.update()
    except Exception as e:
        logger.debug(f"Error en batch update: {e}")
