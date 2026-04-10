"""
Módulo: database.py
Propósito: Capa de persistencia centralizada para E.E.D.A. (SQLite3).
Política (Cot.md): NINGÚN módulo o componente debe acceder directamente a la DB.
Toda interacción debe realizarse a través de esta clase.
"""

import sqlite3
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Ruta canónica de la base de datos (relativa al directorio src/)
_BASE_DIR = Path(__file__).resolve().parent.parent
_DEFAULT_DB_NAME = "isla_digital.db"


class DatabaseManager:
    """
    Gestiona la persistencia de respuestas, progreso y estado del usuario.

    Usa SQLite3 con WAL (Write-Ahead Log) para mejorar la concurrencia.
    Todas las tablas se crean automáticamente si no existen.
    """

    def __init__(self, db_name: str = _DEFAULT_DB_NAME) -> None:
        """
        Inicializa el gestor apuntando al archivo SQLite correcto.

        Args:
            db_name: Nombre del archivo de base de datos dentro del directorio src/.
        """
        self.db_path = str(_BASE_DIR / db_name)
        self._init_db()

    # ──────────────────────────────────────────────────────────────────────────
    # INICIALIZACIÓN
    # ──────────────────────────────────────────────────────────────────────────

    def _init_db(self) -> None:
        """Crea las tablas necesarias si no existen y activa el modo WAL."""
        conn = self._get_conn()
        try:
            # WAL mejora el rendimiento en escrituras concurrentes
            conn.execute("PRAGMA journal_mode=WAL;")
            with conn:
                conn.executescript("""
                    CREATE TABLE IF NOT EXISTS challenge_responses (
                        id        INTEGER PRIMARY KEY AUTOINCREMENT,
                        protocol  TEXT    NOT NULL,
                        unit_id   TEXT    NOT NULL,
                        response  TEXT    NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );

                    CREATE TABLE IF NOT EXISTS user_progress (
                        protocol TEXT NOT NULL,
                        unit_id  TEXT NOT NULL,
                        status   TEXT NOT NULL DEFAULT 'COMPLETED',
                        PRIMARY KEY (protocol, unit_id)
                    );
                """)
        except sqlite3.Error as e:
            logger.error("Error inicializando la base de datos: %s", e)
        finally:
            conn.close()

    # ──────────────────────────────────────────────────────────────────────────
    # CONEXIÓN
    # ──────────────────────────────────────────────────────────────────────────

    def _get_conn(self) -> sqlite3.Connection:
        """
        Crea y retorna una nueva conexión a la base de datos.
        Se usa check_same_thread=False para compatibilidad con async.
        """
        return sqlite3.connect(self.db_path, check_same_thread=False)

    # ──────────────────────────────────────────────────────────────────────────
    # OPERACIONES DE RESPUESTAS
    # ──────────────────────────────────────────────────────────────────────────

    def save_response(self, protocol: str, unit_id: str, response: str) -> bool:
        """
        Guarda la respuesta de un usuario para un desafío de unidad.

        Args:
            protocol: Protocolo activo ("alpha", "delta", "omega").
            unit_id:  Identificador de la unidad pedagógica.
            response: Texto de respuesta del usuario.

        Returns:
            True si se guardó correctamente, False en caso de error.
        """
        if not response.strip():
            return False
        conn = self._get_conn()
        try:
            with conn:
                conn.execute(
                    "INSERT INTO challenge_responses (protocol, unit_id, response) VALUES (?, ?, ?)",
                    (protocol, unit_id, response.strip()),
                )
            return True
        except sqlite3.Error as e:
            logger.error("Error guardando respuesta [%s/%s]: %s", protocol, unit_id, e)
            return False
        finally:
            conn.close()

    def get_responses(self, unit_id: str | None = None) -> list[tuple]:
        """
        Recupera respuestas guardadas, opcionalmente filtradas por unidad.

        Args:
            unit_id: Filtro opcional por unidad pedagógica.

        Returns:
            Lista de tuplas (protocol/unit_id, response, timestamp).
        """
        conn = self._get_conn()
        try:
            with conn:
                if unit_id:
                    rows = conn.execute(
                        "SELECT protocol, response, timestamp FROM challenge_responses WHERE unit_id = ?",
                        (unit_id,),
                    ).fetchall()
                else:
                    rows = conn.execute(
                        "SELECT unit_id, response, timestamp FROM challenge_responses"
                    ).fetchall()
            return rows
        except sqlite3.Error as e:
            logger.error("Error recuperando respuestas: %s", e)
            return []
        finally:
            conn.close()

    # ──────────────────────────────────────────────────────────────────────────
    # OPERACIONES DE PROGRESO
    # ──────────────────────────────────────────────────────────────────────────

    def update_progress(self, protocol: str, unit_id: str, status: str = "COMPLETED") -> bool:
        """
        Registra o actualiza el estado de progreso de una unidad para un protocolo.

        Args:
            protocol: Protocolo activo.
            unit_id:  Identificador de la unidad pedagógica.
            status:   Estado del progreso (por defecto "COMPLETED").

        Returns:
            True si se actualizó correctamente, False en caso de error.
        """
        conn = self._get_conn()
        try:
            with conn:
                conn.execute(
                    "INSERT OR REPLACE INTO user_progress (protocol, unit_id, status) VALUES (?, ?, ?)",
                    (protocol, unit_id, status),
                )
            return True
        except sqlite3.Error as e:
            logger.error("Error actualizando progreso [%s/%s]: %s", protocol, unit_id, e)
            return False
        finally:
            conn.close()

    def get_progress(self, protocol: str) -> list[str]:
        """
        Retorna una lista de unit_ids completadas para un protocolo dado.

        Args:
            protocol: Protocolo a consultar.

        Returns:
            Lista de identificadores de unidades completadas.
        """
        conn = self._get_conn()
        try:
            with conn:
                rows = conn.execute(
                    'SELECT unit_id FROM user_progress WHERE protocol = ? AND status = "COMPLETED"',
                    (protocol,),
                ).fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            logger.error("Error obteniendo progreso de protocolo '%s': %s", protocol, e)
            return []
        finally:
            conn.close()

    def reset_progress(self, protocol: str) -> bool:
        """
        Elimina todo el progreso de un protocolo específico.
        Útil para reiniciar la sesión del usuario.

        Args:
            protocol: Protocolo cuyo progreso se va a eliminar.

        Returns:
            True si se eliminó correctamente, False en caso de error.
        """
        conn = self._get_conn()
        try:
            with conn:
                conn.execute(
                    "DELETE FROM user_progress WHERE protocol = ?",
                    (protocol,),
                )
            return True
        except sqlite3.Error as e:
            logger.error("Error reiniciando progreso de protocolo '%s': %s", protocol, e)
            return False
        finally:
            conn.close()


# ──────────────────────────────────────────────────────────────────────────────
# Instancia global singleton — importar desde todos los módulos que lo necesiten
# ──────────────────────────────────────────────────────────────────────────────
db = DatabaseManager()

# Alias para compatibilidad
Database = DatabaseManager
