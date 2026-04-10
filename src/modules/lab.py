"""
Módulo: lab.py  (modules/)
Archivo desarrollado por Yoangel Gómez
Propósito: Laboratorio interactivo con actividades prácticas para cada protocolo.
Política (Cot.md): Las actividades disponibles se filtran por protocolo activo.
Colores y estilos desde DesignTokens. Lógica separada de presentación.

Actividades:
    - drawing   → Alpha  → Canvas de dibujo libre
    - keyboard  → Delta/Omega → Reto de velocidad de escritura de código
    - logic     → Alpha/Delta/Omega → Secuencia de arranque
"""

import flet as ft
import flet.canvas as cv
import time
import random

from base.module import BaseModule
from core.theme import DesignTokens
from components.glass_container import GlassContainer


# Definición de actividades por protocolo
_ACTIVITIES = [
    {
        "id":        "drawing",
        "title":     "Taller de Diseño y Construcción",
        "icon":      ft.Icons.BRUSH_ROUNDED,
        "desc":      "Dibuja, modela y da vida a tus ideas en el canvas libre.",
        "protocols": ["alpha", "delta", "omega"],
    },
    {
        "id":        "keyboard",
        "title":     "Código Rápido",
        "icon":      ft.Icons.KEYBOARD_ROUNDED,
        "desc":      "Entrena tu velocidad escribiendo código real.",
        "protocols": ["delta", "omega"],
    },
    {
        "id":        "logic",
        "title":     "Reto de Lógica",
        "icon":      ft.Icons.EXTENSION_ROUNDED,
        "desc":      "Ordena los componentes para encender el sistema.",
        "protocols": ["alpha", "delta", "omega"],
    },
    {
        "id":        "bug_hunter",
        "title":     "Cazador de Virus",
        "icon":      ft.Icons.PEST_CONTROL_ROUNDED,
        "desc":      "¡Atrapa a los virus antes de que infecten el sistema!",
        "protocols": ["alpha"],
    },
    {
        "id":        "matrix",
        "title":     "Decodificador de Matriz",
        "icon":      ft.Icons.GRID_VIEW_ROUNDED,
        "desc":      "Encuentra las secuencias ocultas en el flujo de datos.",
        "protocols": ["delta", "omega"],
    },
]

# Fragmentos de código para el reto de teclado
_KEYBOARD_CODES = [
    "print('E.E.D.A._V4_ONLINE')",
    "for chunk in data_stream: process(chunk)",
    "if security.is_active(): access_granted()",
    "def firewall_scan(host: str) -> bool: return True",
    "import crypto.core as cc",
    "kernel.load_module('SECURITY_GATE_v2')",
    "chmod 755 /var/www/html/secure_vault",
    "sudo iptables -A INPUT -p tcp --dport 22 -j DROP",
    "SELECT * FROM users WHERE clearance_level = 'OMEGA';",
    "export E.E.D.A._AUTH_TOKEN='x9f8b7$kL2'",
    "while not system.shutdown(): monitor_nodes()",
    "class CryptoNode(BaseSecureModule): pass",
    "match packet.protocol: case 'TCP': forward()",
    "return payload.encode('utf-8')",
    "git commit -m 'feat: implemented zero-trust architecture'",
]

# Componentes para el reto de lógica (secuencia de arranque)
_LOGIC_ICONS = [
    ft.Icons.POWER,
    ft.Icons.MEMORY,
    ft.Icons.DNS,
    ft.Icons.TERMINAL,
    ft.Icons.SECURITY,
]


class Lab(BaseModule):
    """
    Módulo Lab — Laboratorio interactivo con actividades prácticas.

    Muestra un selector de actividades y, al iniciar una, sustituye la vista
    por el laboratorio correspondiente. Usa cleanup() y reset para regresar al selector.
    """

    def __init__(self, navigation_manager=None, protocol: str = "alpha") -> None:
        super().__init__(navigation_manager, protocol)
        self.protocol_color    = DesignTokens.get_protocol_color(protocol)
        self.active_activity   = None
        self.immersive_mode    = False

        # Estado para el laboratorio de dibujo (Alpha)
        self.canvas = cv.Canvas(
            on_resize=self._on_canvas_resize,
            expand=True,
        )
        self.current_stroke: list = []
        self.drawing_color: str   = self.protocol_color

        # Estado para el reto de teclado (Delta/Omega)
        # Gamificación: Teclado
        self.kb_score: int         = 0
        self.kb_streak: int        = 0
        self.target_text: str      = random.choice(_KEYBOARD_CODES)
        self.typed_text: str       = ""
        self.start_time: float     = 0.0
        self.wpm: int              = 0

        # Gamificación: Lógica
        self.logic_level: int      = 1
        self.logic_sequence: list  = []
        self.user_sequence: list   = []
        self.logic_status: str     = ""

        # Gamificación: Bug Hunter (Alpha)
        self.bh_score: int         = 0
        self.bh_bugs_caught: int   = 0
        self.bh_active_bug: int    = -1
        # Gamificación: Matrix Decoder (Delta/Omega)
        self.matrix_grid: list[int] = []
        self.matrix_target: list[int] = []
        self.matrix_user: list[int] = []
        self.matrix_status: str = "MEMORIZA LA SECUENCIA"
        self.matrix_showing: bool = False

        self.initialize()

    # ──────────────────────────────────────────────────────────────────────────
    # CONSTRUCCIÓN — DESPACHADOR DE VISTAS
    # ──────────────────────────────────────────────────────────────────────────

    def build(self) -> ft.Control:
        if self.active_activity == "drawing":
            return self._build_drawing_lab()
        elif self.active_activity == "keyboard":
            return self._build_keyboard_lab()
        elif self.active_activity == "logic":
            return self._build_logic_lab()
        elif self.active_activity == "bug_hunter":
            return self._build_bug_hunter()
        elif self.active_activity == "matrix":
            return self._build_matrix_decoder()
        return self._build_selector()

    # ──────────────────────────────────────────────────────────────────────────
    # SELECTOR DE ACTIVIDADES
    # ──────────────────────────────────────────────────────────────────────────

    def _build_selector(self) -> ft.Column:
        """Vista principal con tarjetas de actividades disponibles para el protocolo."""
        cards = []
        for act in _ACTIVITIES:
            if self.protocol not in act["protocols"]:
                continue
            cards.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(act["icon"], size=24, color=self.protocol_color),
                            ft.Column(
                                [
                                    ft.Text(
                                        act["title"],
                                        weight="bold",
                                        size=14,
                                        color=DesignTokens.get_text_main(self.protocol),
                                    ),
                                    ft.Text(
                                        act["desc"],
                                        size=11,
                                        color=DesignTokens.get_text_dim(self.protocol),
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=14, color=self.protocol_color),
                        ],
                        spacing=15,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.04, self.protocol_color),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.1, self.protocol_color)),
                    border_radius=8,
                    ink=True,
                    on_click=lambda _, a=act["id"]: self._start_activity(a),
                )
            )

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCIENCE, color=self.protocol_color, size=20),
                        ft.Text(
                            "Laboratorio Interactivo",
                            size=20,
                            weight="bold",
                            color=self.protocol_color,
                            font_family="JetBrains Mono",
                        ),
                        ft.Container(expand=True),
                        ft.Switch(
                            label="Modo inmersivo",
                            on_change=self._toggle_immersive,
                            active_color=self.protocol_color,
                        ),
                    ]
                ),
                ft.Divider(height=20, color="transparent"),
                ft.Divider(height=20, color="transparent"),
                ft.Container(
                    content=ft.Column(cards, spacing=15),
                    width=800,  # Fomenta el centrado al limitar ancho en pantallas grandes
                ),
            ],
            expand=True,
            horizontal_alignment="center",
        )

    # ──────────────────────────────────────────────────────────────────────────
    # TALLER DE DISEÑO Y CONSTRUCCIÓN — TODOS LOS PROTOCOLOS
    # ──────────────────────────────────────────────────────────────────────────

    def _build_drawing_lab(self) -> ft.Column:
        """Canvas de dibujo libre con paleta de colores — disponible globalmente."""
        gesture_layer = ft.GestureDetector(
            content=ft.Container(
                content=self.canvas,
                border=ft.border.all(2, self.protocol_color),
                border_radius=15,
                bgcolor=ft.Colors.WHITE,
                expand=True,
            ),
            on_pan_start=self._pan_start,
            on_pan_update=self._pan_update,
            drag_interval=10,
            expand=True,
        )

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            ft.Icons.ARROW_BACK,
                            on_click=lambda _: self._reset_lab(),
                            icon_color=self.protocol_color,
                        ),
                        ft.Text(
                            "Taller de Diseño y Construcción",
                            size=16,
                            weight="bold",
                            color=self.protocol_color,
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            ft.Icons.DELETE_SWEEP,
                            on_click=self._clear_canvas,
                            icon_color=DesignTokens.COLORS["warning"],
                        ),
                    ]
                ),
                gesture_layer,
                ft.Row(
                    [
                        self._color_swatch(ft.Colors.RED),
                        self._color_swatch(ft.Colors.BLUE),
                        self._color_swatch(ft.Colors.GREEN),
                        self._color_swatch(ft.Colors.ORANGE),
                        self._color_swatch(ft.Colors.PURPLE),
                        self._color_swatch(ft.Colors.BLACK),
                    ],
                    alignment="center",
                    spacing=20,
                ),
            ],
            expand=True,
            spacing=20,
        )

    def _color_swatch(self, color: str) -> ft.Container:
        """Muestra de color seleccionable en la paleta de dibujo."""
        is_selected = self.drawing_color == color
        return ft.Container(
            width=30,
            height=30,
            bgcolor=color,
            border_radius=15,
            on_click=lambda _, c=color: self._set_drawing_color(c),
            border=ft.border.all(
                3 if is_selected else 1,
                ft.Colors.BLACK if is_selected else ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            ),
        )

    def _set_drawing_color(self, color: str) -> None:
        """Cambia el color activo del pincel."""
        self.drawing_color = color
        self.content = self.build()
        self.update()

    def _on_canvas_resize(self, e) -> None:
        pass  # Reservado para futuras adaptaciones de tamaño

    def _pan_start(self, e: ft.DragStartEvent) -> None:
        """Inicia un nuevo trazo en el canvas."""
        self.current_stroke = []
        self.canvas.shapes.append(
            cv.Path(
                elements=[],
                paint=ft.Paint(
                    color=self.drawing_color,
                    stroke_width=4,
                    style=ft.PaintingStyle.STROKE,
                    stroke_join=ft.StrokeJoin.ROUND,
                    stroke_cap=ft.StrokeCap.ROUND,
                ),
            )
        )

    def _pan_update(self, e: ft.DragUpdateEvent) -> None:
        """Agrega un punto al trazo activo del canvas."""
        if not self.canvas.shapes:
            return
        shape = self.canvas.shapes[-1]
        if not shape.elements:
            shape.elements.append(cv.Path.MoveTo(e.local_x, e.local_y))
        else:
            shape.elements.append(cv.Path.LineTo(e.local_x, e.local_y))
        self.canvas.update()

    def _clear_canvas(self, _) -> None:
        """Limpia todos los trazos del canvas."""
        self.canvas.shapes.clear()
        self.canvas.update()

    # ──────────────────────────────────────────────────────────────────────────
    # LABORATORIO DE TECLADO — DELTA/OMEGA
    # ──────────────────────────────────────────────────────────────────────────

    def _build_keyboard_lab(self) -> ft.Column:
        """Reto de velocidad de escritura de código — Delta y Omega."""
        # Generar nuevo reto si no hay texto activo
        if not self.typed_text and self.start_time == 0.0:
            self.target_text = random.choice(_KEYBOARD_CODES)

        results_text = ft.Text(
            f"Velocidad previa: {self.wpm} PPM" if self.wpm > 0 else "Empieza a escribir...",
            size=16,
            italic=True,
            color=DesignTokens.get_text_dim(self.protocol),
        )

        def on_change(e: ft.ControlEvent) -> None:
            if self.start_time == 0.0:
                self.start_time = time.time()

            self.typed_text = e.data or ""
            
            # Validación visual a tiempo real
            if self.target_text.startswith(self.typed_text):
                t_field.border_color = self.protocol_color
            else:
                t_field.border_color = ft.Colors.RED_400
                
            if self.typed_text == self.target_text:
                elapsed      = time.time() - self.start_time
                word_count   = len(self.target_text) / 5
                new_wpm      = int(word_count / (elapsed / 60)) if elapsed > 0 else 0
                self.wpm     = new_wpm
                
                # Sistema de puntaje
                points = 10 + (self.wpm // 10)
                self.kb_score += points
                self.kb_streak += 1
                
                self.typed_text  = ""
                self.start_time  = 0.0
                self.target_text = random.choice(_KEYBOARD_CODES)
                t_field.value    = ""
                t_field.border_color = self.protocol_color
                results_text.value = f"¡+{points} EXP! Racha: {self.kb_streak} 🔥 | Vel: {self.wpm} PPM"
                self.update() # Full update to change target_text visually
                
            t_field.update()
            results_text.update()

        t_field = ft.TextField(
            label="ESCRIBE EL CÓDIGO",
            on_change=on_change,
            focused_border_color=self.protocol_color,
            border_color=self.protocol_color,
            text_size=20,
            color=self.protocol_color,
            text_style=ft.TextStyle(font_family="JetBrains Mono"),
            autofocus=True,
        )

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            ft.Icons.ARROW_BACK,
                            on_click=lambda _: self._reset_lab(),
                        ),
                        ft.Text(
                            "Entrenamiento de código",
                            size=16,
                            weight="bold",
                            color=self.protocol_color,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(f"XP TOTAL: {self.kb_score}", weight="bold", color=DesignTokens.COLORS["accent"]),
                            padding=10,
                            bgcolor=ft.Colors.with_opacity(0.1, DesignTokens.COLORS["accent"]),
                            border_radius=10,
                        )
                    ],
                    alignment="spaceBetween"
                ),
                ft.Container(height=20),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Escribe esto:",
                                size=11,
                                color=DesignTokens.get_text_dim(self.protocol),
                            ),
                            ft.Text(
                                self.target_text,
                                size=22,
                                weight="bold",
                                font_family="JetBrains Mono",
                                color=self.protocol_color,
                            ),
                        ],
                        spacing=5,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.04, self.protocol_color),
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.protocol_color)),
                    border_radius=8,
                    width=400,
                ),
                ft.Container(height=20),
                t_field,
                ft.Container(height=10),
                results_text,
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True,
        )

    # ──────────────────────────────────────────────────────────────────────────
    # LABORATORIO DE LÓGICA — TODOS LOS PROTOCOLOS
    # ──────────────────────────────────────────────────────────────────────────

    def _build_logic_lab(self) -> ft.Column:
        """Reto de secuencia de arranque — Módulo extendido y gamificado."""
        # Definir niveles de dificultad
        LEVEL_SEQUENCES = {
            1: [ft.Icons.POWER, ft.Icons.MEMORY, ft.Icons.SECURITY],
            2: [ft.Icons.POWER, ft.Icons.MEMORY, ft.Icons.DNS, ft.Icons.TERMINAL],
            3: [ft.Icons.POWER, ft.Icons.MEMORY, ft.Icons.SECURITY, ft.Icons.DNS, ft.Icons.TERMINAL]
        }
        
        current_seq = LEVEL_SEQUENCES.get(self.logic_level, LEVEL_SEQUENCES[3])
        
        if not self.logic_sequence:
            self.logic_sequence = current_seq
            self.user_sequence  = []
            self.logic_status   = f"NIVEL {self.logic_level}: ARRANCA EL SISTEMA EN ORDEN LÓGICO"

        def add_to_sequence(icon) -> None:
            if icon in self.user_sequence:
                return
                
            expected_index = len(self.user_sequence)
            if icon == self.logic_sequence[expected_index]:
                self.user_sequence.append(icon)
                self.logic_status = f"✓ {len(self.user_sequence)}/{len(self.logic_sequence)} EN LÍNEA"
                
                if len(self.user_sequence) == len(self.logic_sequence):
                    if self.logic_level < 3:
                        self.logic_level += 1
                        self.logic_status = f"★★★ ¡NIVEL SUPERADO! AVANZANDO AL NIVEL {self.logic_level} ★★★"
                    else:
                        self.logic_status = "★★★ ¡MAESTRÍA DE RED LOGRADA! SISTEMA 100% OPERATIVO ★★★"
                    self.logic_sequence = [] # Force reset next frame
            else:
                self.logic_status = "✗ ERROR DE PROTOCOLO (SECUENCIA ERRÓNEA). REINICIANDO..."
                self.user_sequence = []
            
            self.content = self.build()
            self.update()

        items = [
            ft.Container(
                content=ft.Icon(icon, size=32, color=self.protocol_color),
                on_click=lambda _, i=icon: add_to_sequence(i),
                padding=25,
                border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.05, self.protocol_color),
                border=ft.border.all(1, ft.Colors.with_opacity(0.2, self.protocol_color)),
                ink=True,
                animate_scale=ft.Animation(150, ft.AnimationCurve.DECELERATE),
            )
            for icon in _LOGIC_ICONS
        ]

        status_color = (
            DesignTokens.COLORS["accent"]
            if "ÉXITO" in self.logic_status
            else DesignTokens.COLORS["critical"]
            if "ERROR" in self.logic_status
            else DesignTokens.get_text_dim(self.protocol)
        )

        user_view = [
            ft.Icon(icon, size=30, color=DesignTokens.COLORS["accent"])
            for icon in self.user_sequence
        ]

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            ft.Icons.ARROW_BACK,
                            on_click=lambda _: self._reset_logic_lab(),
                        ),
                        ft.Text(
                            "Conexión de componentes",
                            size=16,
                            weight="bold",
                            color=self.protocol_color,
                            font_family="JetBrains Mono",
                        ),
                    ]
                ),
                ft.Container(height=20),
                ft.Text(
                    self.logic_status,
                    size=16,
                    weight="bold",
                    color=status_color,
                    font_family="JetBrains Mono",
                ),
                ft.Container(height=20),
                ft.Row(items, alignment="center", spacing=20, wrap=True),
                ft.Container(height=30),
                ft.Text(
                    "Tu secuencia:",
                    size=12,
                    color=DesignTokens.get_text_dim(self.protocol),
                ),
                ft.Row(user_view, alignment="center", spacing=15),
                ft.Container(height=40),
                ft.ElevatedButton(
                    "REINICIAR",
                    on_click=lambda _: self._reset_logic_lab(),
                    bgcolor=DesignTokens.COLORS["critical"],
                    color=ft.Colors.WHITE,
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True,
        )

    # ──────────────────────────────────────────────────────────────────────────
    # LABORATORIO ALPHA — CAZADOR DE BUGS (NUEVO MINIJUEGO GAMIFICADO)
    # ──────────────────────────────────────────────────────────────────────────

    def _build_bug_hunter(self) -> ft.Column:
        """Minijuego hiper-interactivo para niños: Atrapar al insecto en la cuadrícula."""
        
        # Generar cuadrícula de 9 (3x3)
        grid_size = 9
        
        # Mover el bug si no hay ninguno activo y el juego no ha terminado
        if self.bh_active_bug == -1 and self.bh_bugs_caught < 10:
            self.bh_active_bug = random.randint(0, grid_size - 1)

        def hit_bug(index: int):
            if index == self.bh_active_bug:
                self.bh_score += 10
                self.bh_bugs_caught += 1
                self.bh_active_bug = -1
                self.content = self.build()
                self.update()
        
        def reset_hunter(_):
            self.bh_score = 0
            self.bh_bugs_caught = 0
            self.bh_active_bug = -1
            self.content = self.build()
            self.update()

        status_msg = "¡Atrapa 10 bichos!" if self.bh_bugs_caught < 10 else "🏆 ¡SISTEMA LIMPIO Y SEGURO! 🏆"
        
        grid_controls = []
        for i in range(grid_size):
            is_bug = (i == self.bh_active_bug)
            
            icon = ft.Icons.BUG_REPORT_ROUNDED if is_bug else ft.Icons.SHIELD_ROUNDED
            color = ft.Colors.RED_ACCENT_400 if is_bug else ft.Colors.with_opacity(0.1, self.protocol_color)
            bg_color = ft.Colors.with_opacity(0.1, ft.Colors.RED) if is_bug else ft.Colors.with_opacity(0.02, self.protocol_color)
            
            grid_controls.append(
                ft.Container(
                    content=ft.Icon(icon, size=40 if is_bug else 20, color=color),
                    alignment=ft.alignment.center,
                    width=100,
                    height=100,
                    bgcolor=bg_color,
                    border_radius=15,
                    border=ft.border.all(2, color) if is_bug else None,
                    on_click=lambda _, idx=i: hit_bug(idx),
                    ink=True,
                    animate_scale=ft.Animation(200, "bounceOut"),
                    scale=1.1 if is_bug else 1.0, # Efecto de "respiración" simulado
                )
            )

        return ft.Column(
            [
                # Header del Minijuego
                ft.Row(
                    [
                        ft.IconButton(
                            ft.Icons.ARROW_BACK,
                            on_click=lambda _: self._reset_lab(),
                            icon_color=self.protocol_color,
                        ),
                        ft.Text(
                            "🧹 Cazador de Virus Espaciales",
                            size=20,
                            weight="bold",
                            color=self.protocol_color,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            content=ft.Text(f"⭐ PUNTOS: {self.bh_score}", weight="bold", size=18, color=ft.Colors.AMBER),
                            padding=15,
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.AMBER),
                            border_radius=15,
                        )
                    ],
                    alignment="spaceBetween"
                ),
                ft.Divider(height=20, color="transparent"),
                
                # Estado Centralizado
                ft.Text(
                    status_msg,
                    size=24,
                    weight="bold",
                    color=ft.Colors.GREEN_400 if self.bh_bugs_caught >= 10 else self.protocol_color,
                    text_align="center"
                ),
                ft.ProgressBar(value=self.bh_bugs_caught / 10, color=ft.Colors.GREEN_400, bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.GREEN_400), width=320, height=10),
                
                ft.Divider(height=20, color="transparent"),
                
                # Cuadrícula de Juego
                ft.Row(
                    [
                        ft.Column([grid_controls[0], grid_controls[1], grid_controls[2]], spacing=15),
                        ft.Column([grid_controls[3], grid_controls[4], grid_controls[5]], spacing=15),
                        ft.Column([grid_controls[6], grid_controls[7], grid_controls[8]], spacing=15),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15
                ),
                
                ft.Divider(height=20, color="transparent"),
                
                # Botón de reinicio si gana
                ft.ElevatedButton(
                    "Jugar Otra Vez 🚀",
                    icon=ft.Icons.REPLAY_ROUNDED,
                    on_click=reset_hunter,
                    visible=self.bh_bugs_caught >= 10,
                    style=ft.ButtonStyle(padding=20, shape=ft.RoundedRectangleBorder(radius=10), bgcolor=self.protocol_color, color="white")
                )
            ],
            horizontal_alignment="center",
            expand=True
        )

    # ──────────────────────────────────────────────────────────────────────────
    # HELPERS Y EVENTOS
    # ──────────────────────────────────────────────────────────────────────────

    def _toggle_immersive(self, e: ft.ControlEvent) -> None:
        """Activa/desactiva el modo inmersivo (oculta el sidebar)."""
        self.immersive_mode = e.control.value
        if self.nav and self.nav.sidebar:
            self.nav.sidebar.visible = not self.immersive_mode
            try:
                self.nav.app_page.update()
            except Exception:
                pass
        self.update()

    def _start_activity(self, activity_id: str) -> None:
        """Inicia la actividad seleccionada."""
        self.active_activity = activity_id
        self.content = self.build()
        self.update()

    def _reset_lab(self) -> None:
        """Vuelve al selector de actividades y reinicia el estado del teclado."""
        self.active_activity = None
        self.typed_text      = ""
        self.start_time      = 0.0
        self.content         = self.build()
        self.update()

    def _build_matrix_decoder(self) -> ft.Column:
        """Minijuego de memoria para Delta/Omega."""
        grid_size = 16 # 4x4
        
        if not self.matrix_grid:
            self.matrix_grid = list(range(grid_size))
            self.matrix_target = random.sample(self.matrix_grid, 5)
            self.matrix_user = []
            self.matrix_showing = True
            
            # Timer para ocultar la secuencia (usa async en lugar de threading)
            async def hide_sequence():
                import asyncio
                await asyncio.sleep(2)
                self.matrix_showing = False
                self.matrix_status = "¡REPRODUCE LA SECUENCIA!"
                try:
                    self.content = self.build()
                    self.update()
                except Exception:
                    pass
            
            try:
                self.page.run_task(hide_sequence)
            except Exception:
                pass

        def on_click(idx):
            if self.matrix_showing: return
            if idx in self.matrix_user: return
            
            self.matrix_user.append(idx)
            
            # Verificar
            if self.matrix_user == self.matrix_target[:len(self.matrix_user)]:
                if len(self.matrix_user) == len(self.matrix_target):
                    self.matrix_status = "🔓 ¡ACCESO CONCEDIDO! MATRIZ DECODIFICADA"
                    self.kb_score += 50
                    # Reiniciar tras un momento
                    async def reset():
                        import asyncio
                        await asyncio.sleep(1.5)
                        self.matrix_grid = []
                        try:
                            self.content = self.build()
                            self.update()
                        except Exception:
                            pass
                    try:
                        self.page.run_task(reset)
                    except Exception:
                        pass
            else:
                self.matrix_status = "🔒 ERROR DE DECODIFICACIÓN. REINICIANDO..."
                self.matrix_user = []
                async def fail_reset():
                    import asyncio
                    await asyncio.sleep(1)
                    self.matrix_grid = []
                    try:
                        self.content = self.build()
                        self.update()
                    except Exception:
                        pass
                try:
                    self.page.run_task(fail_reset)
                except Exception:
                    pass
            try:
                self.content = self.build()
                self.update()
            except Exception:
                pass

        grid_controls = []
        for i in range(grid_size):
            is_target = i in self.matrix_target and self.matrix_showing
            is_user = i in self.matrix_user
            
            color = self.protocol_color if (is_target or is_user) else ft.Colors.with_opacity(0.1, self.protocol_color)
            
            grid_controls.append(
                ft.Container(
                    width=60, height=60,
                    bgcolor=color,
                    border_radius=8,
                    animate_scale=300,
                    on_click=lambda _, idx=i: on_click(idx),
                )
            )

        return ft.Column(
            [
                ft.Row([
                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: self._reset_lab()),
                    ft.Text("Decodificador de Matriz", size=20, weight="bold", color=self.protocol_color),
                ]),
                ft.Container(height=40),
                ft.Text(self.matrix_status, size=18, weight="bold", color=self.protocol_color),
                ft.Container(height=20),
                ft.GridView(
                    grid_controls,
                    runs_count=4,
                    max_extent=80,
                    spacing=10,
                    run_spacing=10,
                    width=320,
                ),
            ],
            horizontal_alignment="center",
            alignment="center",
        )

    def _reset_logic_lab(self) -> None:
        """Reinicia el reto de lógica y vuelve al selector."""
        self.logic_sequence = []
        self.user_sequence  = []
        self.logic_status   = ""
        self.matrix_grid    = [] 
        self.matrix_user    = []
        self.matrix_status  = "MEMORIZA LA SECUENCIA"
        self._reset_lab()
