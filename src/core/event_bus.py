"""
Módulo: event_bus.py
Propósito: Bus de eventos centralizado y desacoplado para comunicación entre módulos E.E.D.A.
Política: Toda comunicación entre módulos DEBE usar este bus. Sin referencias cruzadas directas.
"""

import collections
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)


class EventBus:
    """
    Bus de eventos global con soporte para suscripción, desuscripción y emisión de eventos.
    Implementa el patrón Observer/Pub-Sub de forma desacoplada.
    """

    def __init__(self):
        self._listeners: dict[str, list[Callable]] = collections.defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Registra un callback para un tipo de evento.

        Args:
            event_type: Nombre del evento (p. ej., 'nav_change', 'protocol_set').
            callback: Función a invocar cuando se emita el evento.
        """
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """
        Elimina un callback previamente registrado para evitar fugas de memoria.

        Args:
            event_type: Tipo de evento del que desuscribirse.
            callback: Función que se desea eliminar.
        """
        try:
            self._listeners[event_type].remove(callback)
        except ValueError:
            pass  # El callback ya no estaba registrado

    def emit(self, event_type: str, data: Any = None) -> None:
        """
        Emite un evento a todos los suscriptores registrados.

        Args:
            event_type: Tipo de evento a emitir.
            data: Datos opcionales asociados al evento.
        """
        listeners = list(self._listeners.get(event_type, []))
        for callback in listeners:
            try:
                callback(data)
            except Exception as e:
                logger.error("Error en listener de evento '%s': %s", event_type, e)

    def clear(self, event_type: str | None = None) -> None:
        """
        Limpia todos los listeners de un evento específico o de todos los eventos.

        Args:
            event_type: Si se provee, solo elimina listeners de ese evento.
                        Si es None, limpia todo el bus.
        """
        if event_type:
            self._listeners.pop(event_type, None)
        else:
            self._listeners.clear()


# Instancia global singleton — importar desde todos los módulos
bus = EventBus()
