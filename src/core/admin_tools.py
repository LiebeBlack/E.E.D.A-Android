"""
Módulo: admin_tools.py
Propósito: Herramientas de desarrollador y administrador para E.E.D.A.
"""

from typing import TYPE_CHECKING
import sys
import time
import platform

import flet as ft

from core.theme import DesignTokens
from core.config import GOLD_ACCENT, config
from core.utils import safe_update, close_all_overlays, truncate_text
from core.database import db
from core.content import ContentEngine
from core.event_bus import bus

if TYPE_CHECKING:
    from main import App


class AdminTools:
    """
    Herramientas de administración y desarrollo para E.E.D.A.
    
    Incluye:
        - Inspector del sistema
        - Visor de base de datos
        - Gestor de progreso
        - Mapa de contenido
        - Monitor de event bus
        - Navegación rápida
        - Consola de debug
        - Theme lab
    """
    
    def __init__(self, app: "App") -> None:
        self.app = app
        self.page = app.app_page
        self.gold = GOLD_ACCENT
    
    def build_admin_panel(
        self,
        theme_section: ft.Container,
        audio_panel: ft.Container,
        anim_panel: ft.Container,
        dev_node: ft.Container
    ) -> ft.Column:
        """Construye el panel completo de administrador."""
        
        return ft.Column([
            self._build_admin_badge(),
            theme_section,
            audio_panel,
            anim_panel,
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.15, self.gold)),
            ft.Text(
                "⚡ HERRAMIENTAS DE DESARROLLADOR",
                size=11,
                weight="bold",
                color=self.gold,
                font_family=config.font_mono
            ),
            self._build_sys_inspector(),
            self._build_quick_nav(),
            self._build_db_viewer(),
            self._build_progress_mgr(),
            self._build_content_map(),
            self._build_event_monitor(),
            self._build_theme_lab(),
            self._build_debug_console(),
            ft.Divider(height=1, color=ft.Colors.with_opacity(0.15, self.gold)),
            dev_node,
            ft.Container(height=8),
            ft.Row([
                ft.Text(
                    f"V {config.version}",
                    size=9,
                    weight="bold",
                    color=self.gold,
                    font_family=config.font_mono
                ),
                ft.Container(expand=True),
                ft.Text("E.E.D.A. — Admin Console", size=10, italic=True, color=self.gold),
            ])
        ], spacing=14, width=540, height=720, scroll=ft.ScrollMode.HIDDEN)
    
    def _build_admin_badge(self) -> ft.Container:
        """Badge de modo administrador."""
        
        def logout_admin(_: ft.ControlEvent) -> None:
            self.app.is_admin = False
            config.version.suffix = "STABLE"
            close_all_overlays(self.page)
            # Reabrir como visitante
            from core.settings_manager import SettingsManager
            SettingsManager(self.app).show_settings(None)
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, color=self.gold, size=18),
                ft.Text(
                    "MODO ADMINISTRADOR",
                    size=12,
                    weight="bold",
                    color=self.gold,
                    font_family=config.font_mono
                ),
                ft.Container(expand=True),
                ft.TextButton(
                    "Cerrar Sesión",
                    icon=ft.Icons.LOGOUT_ROUNDED,
                    on_click=logout_admin,
                    style=ft.ButtonStyle(color=DesignTokens.COLORS["critical"])
                ),
            ], spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            bgcolor=ft.Colors.with_opacity(0.1, self.gold),
            border_radius=12,
            border=ft.border.all(1.5, ft.Colors.with_opacity(0.3, self.gold)),
        )
    
    def _build_sys_inspector(self) -> ft.Container:
        """Inspector del sistema con información técnica."""
        
        flet_ver = "N/A"
        try:
            flet_ver = ft.version.version
        except Exception:
            pass
        
        sys_info = [
            ("Python", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"),
            ("Flet", flet_ver),
            ("OS", f"{platform.system()} {platform.release()}"),
            ("Protocolo", (self.app.age_protocol or "N/A").upper()),
            ("Módulo Activo", type(self.app.active_module_instance).__name__ if self.app.active_module_instance else "None"),
            ("Tema", str(self.page.theme_mode).split(".")[-1]),
            ("Animaciones", self.app.anim_intensity),
            ("Vol. Maestro", f"{int(self.app.master_volume * 100)}%"),
            ("Vol. SFX", f"{int(self.app.sfx_volume * 100)}%"),
            ("Admin", "✓ ACTIVO"),
            ("DB Path", truncate_text(db.db_path, 35)),
            ("Navegación", f"{len(self.app._nav_history)} items en historial"),
        ]
        
        text_main = DesignTokens.get_text_main(self.app.age_protocol or "alpha")
        
        sys_rows = [
            ft.Row([
                ft.Text(lbl, size=10, weight="bold", color=self.gold, width=110, font_family=config.font_mono),
                ft.Text(val, size=10, color=text_main, font_family=config.font_mono),
            ], spacing=8)
            for lbl, val in sys_info
        ]
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.DEVELOPER_BOARD_ROUNDED, color=self.gold, size=16),
                    ft.Text(
                        "INSPECTOR DEL SISTEMA",
                        size=10,
                        weight="bold",
                        color=self.gold,
                        font_family=config.font_mono
                    )
                ], spacing=8),
                ft.Container(height=6),
                *sys_rows,
            ], spacing=3),
            padding=14,
            bgcolor=ft.Colors.with_opacity(0.06, self.gold),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.gold)),
        )
    
    def _build_db_viewer(self) -> ft.Container:
        """Visor de base de datos."""
        
        db_output = ft.Text("", font_family=config.font_mono, size=10, 
                          color=DesignTokens.get_text_main(self.app.age_protocol or "alpha"),
                          selectable=True)
        
        def show_db_progress(_: ft.ControlEvent) -> None:
            lines = []
            for proto in ["alpha", "delta", "omega"]:
                progress = db.get_progress(proto)
                lines.append(f"[{proto.upper()}] Completadas: {len(progress)}")
                for uid in progress:
                    lines.append(f"  ✓ {uid}")
            db_output.value = "\n".join(lines) if lines else "Sin progreso registrado."
            safe_update(self.page)
        
        def show_db_responses(_: ft.ControlEvent) -> None:
            responses = db.get_responses()
            lines = []
            for row in responses[:20]:
                lines.append(f"[{row[0]}] {truncate_text(str(row[1]), 60)}")
                if len(row) > 2:
                    lines.append(f"  📅 {row[2]}")
            db_output.value = "\n".join(lines) if lines else "Sin respuestas guardadas."
            safe_update(self.page)
        
        def show_db_stats(_: ft.ControlEvent) -> None:
            lines = ["=== ESTADÍSTICAS DB ==="]
            total_progress = 0
            for proto in ["alpha", "delta", "omega"]:
                prog = db.get_progress(proto)
                total_progress += len(prog)
                lines.append(f"  [{proto.upper()}] {len(prog)} unidades completadas")
            responses = db.get_responses()
            lines.extend([
                f"\n  Total progreso: {total_progress}",
                f"  Total respuestas: {len(responses)}",
                f"  DB: {truncate_text(db.db_path, 40)}"
            ])
            db_output.value = "\n".join(lines)
            safe_update(self.page)
        
        def clear_db_output(_: ft.ControlEvent) -> None:
            db_output.value = ""
            safe_update(self.page)
        
        def make_btn(text: str, icon: str, on_click) -> ft.ElevatedButton:
            return ft.ElevatedButton(
                text,
                icon=getattr(ft.Icons, icon),
                on_click=on_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=8,
                    bgcolor=ft.Colors.with_opacity(0.1, self.gold)
                )
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.STORAGE_ROUNDED, color=self.gold, size=16),
                    ft.Text(
                        "VISOR DE BASE DE DATOS",
                        size=10,
                        weight="bold",
                        color=self.gold,
                        font_family=config.font_mono
                    )
                ], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    make_btn("Progreso", "CHECKLIST_ROUNDED", show_db_progress),
                    make_btn("Respuestas", "QUESTION_ANSWER_ROUNDED", show_db_responses),
                    make_btn("Stats", "ANALYTICS_ROUNDED", show_db_stats),
                    ft.IconButton(
                        ft.Icons.CLEAR_ALL_ROUNDED,
                        icon_color=DesignTokens.get_text_dim(self.app.age_protocol or "alpha"),
                        on_click=clear_db_output,
                        tooltip="Limpiar"
                    ),
                ], spacing=6, wrap=True),
                ft.Container(
                    content=ft.Column([db_output], scroll=ft.ScrollMode.AUTO),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.04, self.gold),
                    border_radius=8,
                    height=120,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.gold)),
                ),
            ], spacing=4),
            padding=14,
            bgcolor=ft.Colors.with_opacity(0.06, self.gold),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.gold)),
        )
    
    def _build_progress_mgr(self) -> ft.Container:
        """Gestor de progreso del usuario."""
        
        progress_status = ft.Text("", font_family=config.font_mono, size=10, color=self.gold)
        
        def unlock_all_units(_: ft.ControlEvent) -> None:
            proto = self.app.age_protocol
            units = ContentEngine.get_all_units(proto)
            for unit in units:
                db.update_progress(proto, unit["id"])
            progress_status.value = f"✓ {len(units)} unidades desbloqueadas para [{proto.upper()}]"
            safe_update(self.page)
        
        def unlock_all_protocols(_: ft.ControlEvent) -> None:
            count = 0
            for proto in ["alpha", "delta", "omega"]:
                units = ContentEngine.get_all_units(proto)
                for unit in units:
                    db.update_progress(proto, unit["id"])
                count += len(units)
            progress_status.value = f"✓ {count} unidades desbloqueadas en TODOS los protocolos"
            safe_update(self.page)
        
        def reset_current_progress(_: ft.ControlEvent) -> None:
            db.reset_progress(self.app.age_protocol)
            progress_status.value = f"✓ Progreso eliminado para [{self.app.age_protocol.upper()}]"
            safe_update(self.page)
        
        def reset_all_progress(_: ft.ControlEvent) -> None:
            for proto in ["alpha", "delta", "omega"]:
                db.reset_progress(proto)
            progress_status.value = "✓ Progreso eliminado para TODOS los protocolos."
            safe_update(self.page)
        
        def make_btn(content: ft.Row, on_click, bgcolor: str) -> ft.ElevatedButton:
            return ft.ElevatedButton(
                content=content,
                on_click=on_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=10,
                    bgcolor=bgcolor,
                    color="white"
                )
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TUNE_ROUNDED, color=self.gold, size=16),
                    ft.Text(
                        "GESTOR DE PROGRESO",
                        size=10,
                        weight="bold",
                        color=self.gold,
                        font_family=config.font_mono
                    )
                ], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    make_btn(
                        ft.Row([ft.Icon(ft.Icons.LOCK_OPEN_ROUNDED, size=14), ft.Text("Desbloquear Actual", size=11)], spacing=4),
                        unlock_all_units,
                        DesignTokens.COLORS["accent"]
                    ),
                    make_btn(
                        ft.Row([ft.Icon(ft.Icons.KEY_ROUNDED, size=14), ft.Text("Desbloquear Todo", size=11)], spacing=4),
                        unlock_all_protocols,
                        "#00B4D8"
                    ),
                ], spacing=6, wrap=True),
                ft.Row([
                    make_btn(
                        ft.Row([ft.Icon(ft.Icons.RESTART_ALT_ROUNDED, size=14), ft.Text("Reset Actual", size=11)], spacing=4),
                        reset_current_progress,
                        ft.Colors.ORANGE_700
                    ),
                    make_btn(
                        ft.Row([ft.Icon(ft.Icons.DELETE_FOREVER_ROUNDED, size=14), ft.Text("Reset Global", size=11)], spacing=4),
                        reset_all_progress,
                        DesignTokens.COLORS["critical"]
                    ),
                ], spacing=6, wrap=True),
                progress_status,
            ], spacing=6),
            padding=14,
            bgcolor=ft.Colors.with_opacity(0.06, self.gold),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.gold)),
        )
    
    def _build_content_map(self) -> ft.Container:
        """Mapa de contenido educativo."""
        
        content_lines = []
        for proto in ["alpha", "delta", "omega"]:
            units = ContentEngine.get_all_units(proto)
            content_lines.append(f"[{proto.upper()}] {len(units)} unidades:")
            for u in units:
                quiz_count = len(u.get("quiz", []))
                content_lines.append(f"  • {u['id']}: {u['title']} ({quiz_count}Q)")
        
        text_main = DesignTokens.get_text_main(self.app.age_protocol or "alpha")
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.MAP_ROUNDED, color=self.gold, size=16),
                    ft.Text(
                        "MAPA DE CONTENIDO",
                        size=10,
                        weight="bold",
                        color=self.gold,
                        font_family=config.font_mono
                    )
                ], spacing=8),
                ft.Container(height=6),
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "\n".join(content_lines),
                            font_family=config.font_mono,
                            size=9,
                            color=text_main,
                            selectable=True
                        ),
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.04, self.gold),
                    border_radius=8,
                    height=150,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.gold)),
                ),
            ], spacing=4),
            padding=14,
            bgcolor=ft.Colors.with_opacity(0.06, self.gold),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.gold)),
        )
    
    def _build_event_monitor(self) -> ft.Container:
        """Monitor del bus de eventos."""
        
        event_log_text = ft.Text(
            "Esperando...",
            font_family=config.font_mono,
            size=10,
            color=DesignTokens.get_text_main(self.app.age_protocol or "alpha"),
            selectable=True
        )
        
        def show_bus_state(_: ft.ControlEvent) -> None:
            lines = ["=== EVENT BUS STATE ==="]
            if hasattr(bus, '_listeners') and bus._listeners:
                for event_type, listeners in bus._listeners.items():
                    lines.append(f"  [{event_type}] → {len(listeners)} listener(s)")
            else:
                lines.append("  (vacío — sin suscripciones activas)")
            event_log_text.value = "\n".join(lines)
            safe_update(self.page)
        
        def emit_test_event(_: ft.ControlEvent) -> None:
            bus.emit("admin_test", {"source": "admin_console", "time": time.time()})
            event_log_text.value = f"✓ Evento 'admin_test' emitido a las {time.strftime('%H:%M:%S')}"
            safe_update(self.page)
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CABLE_ROUNDED, color=self.gold, size=16),
                    ft.Text(
                        "MONITOR EVENT BUS",
                        size=10,
                        weight="bold",
                        color=self.gold,
                        font_family=config.font_mono
                    )
                ], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    ft.ElevatedButton(
                        "Ver Estado",
                        icon=ft.Icons.VISIBILITY_ROUNDED,
                        on_click=show_bus_state,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=8,
                            bgcolor=ft.Colors.with_opacity(0.1, self.gold)
                        )
                    ),
                    ft.ElevatedButton(
                        "Emitir Test",
                        icon=ft.Icons.SEND_ROUNDED,
                        on_click=emit_test_event,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=8,
                            bgcolor=ft.Colors.with_opacity(0.1, self.gold)
                        )
                    ),
                ], spacing=6),
                ft.Container(
                    content=ft.Column([event_log_text], scroll=ft.ScrollMode.AUTO),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.04, self.gold),
                    border_radius=8,
                    height=80,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.gold)),
                ),
            ], spacing=4),
            padding=14,
            bgcolor=ft.Colors.with_opacity(0.06, self.gold),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.gold)),
        )
    
    def _build_quick_nav(self) -> ft.Container:
        """Navegación rápida para desarrolladores."""
        
        def nav_to(module_name: str) -> None:
            close_all_overlays(self.page)
            self.app.navigate_to(module_name)
        
        def switch_protocol(proto: str) -> None:
            close_all_overlays(self.page)
            self.app.age_protocol = proto
            p_color = DesignTokens.get_protocol_color(proto)
            self.page.theme = ft.Theme(
                font_family=config.font_main,
                color_scheme=ft.ColorScheme(primary=p_color)
            )
            self.app.build_main_layout()
            self.app.navigate_to("dashboard")
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.SPEED_ROUNDED, color=self.gold, size=16),
                    ft.Text(
                        "NAVEGACIÓN RÁPIDA DEV",
                        size=10,
                        weight="bold",
                        color=self.gold,
                        font_family=config.font_mono
                    )
                ], spacing=8),
                ft.Container(height=6),
                ft.Text("Módulos:", size=9, 
                       color=DesignTokens.get_text_dim(self.app.age_protocol or "alpha"),
                       weight="bold"),
                ft.Row([
                    ft.ElevatedButton("Zones", on_click=lambda _: nav_to("zones")),
                    ft.ElevatedButton("Lab", on_click=lambda _: nav_to("lab")),
                    ft.ElevatedButton("Security", on_click=lambda _: nav_to("security")),
                    ft.ElevatedButton("Dashboard", on_click=lambda _: nav_to("dashboard")),
                ], spacing=6, wrap=True),
                ft.Container(height=4),
                ft.Text("Cambiar Protocolo:", size=9,
                       color=DesignTokens.get_text_dim(self.app.age_protocol or "alpha"),
                       weight="bold"),
                ft.Row([
                    ft.ElevatedButton(
                        "Alpha",
                        on_click=lambda _: switch_protocol("alpha"),
                        style=ft.ButtonStyle(bgcolor=DesignTokens.COLORS["primary"], color="white")
                    ),
                    ft.ElevatedButton(
                        "Delta",
                        on_click=lambda _: switch_protocol("delta"),
                        style=ft.ButtonStyle(bgcolor=DesignTokens.COLORS["secondary"], color="white")
                    ),
                    ft.ElevatedButton(
                        "Omega",
                        on_click=lambda _: switch_protocol("omega"),
                        style=ft.ButtonStyle(bgcolor=DesignTokens.COLORS["critical"], color="white")
                    ),
                ], spacing=6),
            ], spacing=4),
            padding=14,
            bgcolor=ft.Colors.with_opacity(0.06, self.gold),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.gold)),
        )
    
    def _build_theme_lab(self) -> ft.Container:
        """Laboratorio de temas para pruebas de color."""
        
        protocol_color = DesignTokens.get_protocol_color(self.app.age_protocol or "alpha")
        color_preview = ft.Container(width=40, height=40, border_radius=20, bgcolor=protocol_color)
        
        def apply_custom_color(ev: ft.ControlEvent) -> None:
            hex_val = ev.control.value or ""
            if len(hex_val) >= 4 and hex_val.startswith("#"):
                color_preview.bgcolor = hex_val
                self.page.theme = ft.Theme(
                    font_family=config.font_main,
                    color_scheme=ft.ColorScheme(primary=hex_val)
                )
                safe_update(self.page)
        
        def set_preset_color(c: str) -> None:
            color_preview.bgcolor = c
            self.page.theme = ft.Theme(
                font_family=config.font_main,
                color_scheme=ft.ColorScheme(primary=c)
            )
            safe_update(self.page)
        
        presets = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#FF8A5C", "#6C5CE7"]
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PALETTE_ROUNDED, color=self.gold, size=16),
                    ft.Text(
                        "THEME LAB",
                        size=10,
                        weight="bold",
                        color=self.gold,
                        font_family=config.font_mono
                    )
                ], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    ft.Text("Color hex:", size=11, 
                           color=DesignTokens.get_text_main(self.app.age_protocol or "alpha")),
                    ft.TextField(
                        value=protocol_color,
                        width=120,
                        text_size=11,
                        border_radius=8,
                        text_style=ft.TextStyle(font_family=config.font_mono),
                        on_submit=apply_custom_color
                    ),
                    color_preview,
                ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Row([
                    ft.Text("Presets:", size=9,
                           color=DesignTokens.get_text_dim(self.app.age_protocol or "alpha")),
                    *[
                        ft.Container(
                            width=24, height=24, border_radius=12, bgcolor=c,
                            on_click=lambda _, color=c: set_preset_color(color)
                        )
                        for c in presets
                    ],
                ], spacing=6),
            ], spacing=6),
            padding=14,
            bgcolor=ft.Colors.with_opacity(0.06, self.gold),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.gold)),
        )
    
    def _build_debug_console(self) -> ft.Container:
        """Consola de debug para evaluar expresiones Python."""
        
        text_main = DesignTokens.get_text_main(self.app.age_protocol or "alpha")
        debug_output = ft.Text("", font_family=config.font_mono, size=10, color=text_main, selectable=True)
        debug_input = ft.TextField(
            label="Ejecutar expresión Python (eval)",
            text_size=11,
            border_radius=8,
            width=380,
            text_style=ft.TextStyle(font_family=config.font_mono)
        )
        
        def run_debug_expr(_: ft.ControlEvent) -> None:
            expr = debug_input.value or ""
            if not expr.strip():
                return
            
            import os
            try:
                result = eval(expr, {
                    "self": self.app,
                    "ft": ft,
                    "db": db,
                    "bus": bus,
                    "DesignTokens": DesignTokens,
                    "ContentEngine": ContentEngine,
                    "sys": sys,
                    "os": os
                })
                debug_output.value = f">>> {expr}\n{repr(result)}"
            except Exception as ex:
                debug_output.value = f">>> {expr}\n❌ {type(ex).__name__}: {ex}"
            safe_update(self.page)
        
        debug_input.on_submit = run_debug_expr
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TERMINAL_ROUNDED, color=self.gold, size=16),
                    ft.Text(
                        "CONSOLA DE DEBUG",
                        size=10,
                        weight="bold",
                        color=self.gold,
                        font_family=config.font_mono
                    )
                ], spacing=8),
                ft.Container(height=6),
                ft.Row([
                    debug_input,
                    ft.IconButton(
                        ft.Icons.PLAY_ARROW_ROUNDED,
                        icon_color=self.gold,
                        on_click=run_debug_expr,
                        tooltip="Ejecutar"
                    ),
                ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Column([debug_output], scroll=ft.ScrollMode.AUTO),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.04, self.gold),
                    border_radius=8,
                    height=80,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.gold)),
                ),
            ], spacing=4),
            padding=14,
            bgcolor=ft.Colors.with_opacity(0.06, self.gold),
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.gold)),
        )
