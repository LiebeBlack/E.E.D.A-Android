class ContentEngine:
    """
    Motor central de contenido educativo para E.E.D.A.
    Organizado por Protocolo (Edad) y Unidades Pedagógicas.
    """
    
    PROTOCOLS = {
        "alpha": {
            "name": "PROTOCOLO ALPHA",
            "age_range": "3-7 años",
            "description": "Expedición Galáctica Suprema: Conquista de Mundos Digitales",
            "theme_color": "#00FF41"
        },
        "delta": {
            "name": "PROTOCOLO DELTA",
            "age_range": "8-12 años",
            "description": "Lógica Operacional y Seguridad Activa",
            "theme_color": "#00E5FF"
        },
        "omega": {
            "name": "PROTOCOLO OMEGA",
            "age_range": "13-16 años",
            "description": "Arquitectura de Sistemas y Ciberdefensa",
            "theme_color": "#FF3D00"
        }
    }

    DASHBOARD = {
        "alpha": {
            "title": "Centro de Exploración Alpha",
            "labels": ["Oxígeno", "Energía", "Escudo"],
            "mission": "¡Hola, explorador! Tu nave está lista para descubrir nuevos mundos digitales."
        },
        "delta": {
            "title": "Sala de Control Delta",
            "labels": ["CPU", "Red", "Seguridad"],
            "mission": "Agente Delta, todo el sistema está bajo tu supervisión. ¿Listo para la operación?"
        },
        "omega": {
            "title": "Interfaz de Arquitectura Omega",
            "labels": ["Kernel", "Nodos", "Amenazas"],
            "mission": "Arquitecto Omega, la integridad del núcleo depende de tu análisis técnico."
        }
    }

    SECURITY_PRACTICES = {
        "alpha": [
            ("Mantén tu estación limpia y organizada para trabajar mejor.", "CLEANING_SERVICES_ROUNDED"),
            ("Guarda tus herramientas después de usarlas.", "BUILD_ROUNDED"),
            ("Pide ayuda cuando no entiendas algo.", "HELP_ROUNDED"),
        ],
        "delta": [
            ("Documenta cada cambio que hagas en el sistema.", "DESCRIPTION_ROUNDED"),
            ("Haz copias de seguridad antes de modificar archivos.", "SAVE_ROUNDED"),
            ("Verifica tu trabajo antes de aplicar cambios.", "FACT_CHECK_ROUNDED"),
        ],
        "omega": [
            ("Mantén logs detallados de todas las operaciones.", "TEXT_SNIPPET_ROUNDED"),
            ("Prueba en entorno sandbox antes de producción.", "SCIENCE_ROUNDED"),
            ("Automatiza tareas repetitivas para ganar eficiencia.", "AUTO_FIX_ROUNDED"),
        ]
    }

    SECURITY_METRICS = {
        "alpha": {
            "title": "PANEL DE CONTROL // ESTADO",
            "metrics": [
                {"label": "Progreso_Total", "value": "85%", "icon_name": "TRENDING_UP_ROUNDED", "color_key": "accent"},
                {"label": "Tareas_Hechas", "value": "12/15", "icon_name": "CHECKLIST_ROUNDED", "color_key": "primary"},
                {"label": "Nivel_Actual", "value": "EXPLORADOR", "icon_name": "ROCKET_ROUNDED", "color_key": "warning"},
            ]
        },
        "delta": {
            "title": "DASHBOARD DE PRODUCTIVIDAD // MÉTRICAS",
            "metrics": [
                {"label": "Proyectos_Completados", "value": "24", "icon_name": "FOLDER_SPECIAL_ROUNDED", "color_key": "accent"},
                {"label": "Eficiencia", "value": "94%", "icon_name": "SPEED_ROUNDED", "color_key": "primary"},
                {"label": "Rango", "value": "OPERADOR", "icon_name": "ENGINEERING_ROUNDED", "color_key": "warning"},
            ]
        },
        "omega": {
            "title": "CENTRO DE COMANDO // SISTEMA",
            "metrics": [
                {"label": "Módulos_Activos", "value": "156", "icon_name": "APPS_ROUNDED", "color_key": "accent"},
                {"label": "Rendimiento", "value": "99.9%", "icon_name": "MONITORING_ROUNDED", "color_key": "primary"},
                {"label": "Clasificación", "value": "ARQUITECTO", "icon_name": "ARCHITECTURE_ROUNDED", "color_key": "warning"},
            ]
        }
    }

    UNITS = {
        # ═══════════════════════════════════════════════════════════════════════
        # JUEGOS Y HERRAMIENTAS PROFESIONALES POR PROTOCOLO
        # ═══════════════════════════════════════════════════════════════════════
        
        # ─── PROTOCOLO ALPHA: Juegos Educativos Básicos ───
        "memory_master": {
            "icon": "MEMORY",
            "alpha": {
                "title": "Entrenador de Memoria Visual",
                "intro": "Desafía tu cerebro con secuencias de colores, formas y patrones que mejoran tu capacidad de retención.",
                "architecture": "El juego presenta secuencias visuales de forma progresiva. Cada nivel añade más elementos para desafiar tu memoria a corto plazo.",
                "security": "Descansa la vista cada 20 minutos. Mantén una postura cómoda mientras juegas.",
                "challenge": "Completa secuencias de 5, 8, 12, 16 y 20 elementos sin errores.",
                "fact": "La memoria visual es una de las primeras habilidades que desarrollamos. Los niños pueden recordar imágenes más rápido que palabras.",
                "game_type": "memory_sequence",
                "levels": 5,
                "tools": ["Secuenciador de patrones", "Temporizador de reacción", "Medidor de precisión"],
                "quiz": [
                    {"q": "¿Cuántos elementos tiene el nivel máximo?", "a": ["10", "15", "20", "25"], "c": 2},
                    {"q": "¿Qué mejora este entrenamiento?", "a": ["Fuerza física", "Memoria visual y retención", "Velocidad de internet", "Dibujo artístico"], "c": 1}
                ]
            }
        },
        "color_logic": {
            "icon": "PALETTE",
            "alpha": {
                "title": "Laboratorio de Colores y Formas",
                "intro": "Aprende teoría del color básica, mezclas y patrones geométricos mediante puzzles interactivos.",
                "architecture": "Usa la rueda de colores virtual para mezclar primarios y crear secundarios. Cada mezcla exitosa desbloquea nuevas formas.",
                "security": "No mires la pantalla con mucho brillo. Ajusta el volumen a un nivel cómodo.",
                "challenge": "Crea 10 colores diferentes mezclando primarios y secundarios.",
                "fact": "El amarillo es el color que el ojo humano percibe más rápidamente. Por eso los taxis y señales de precaución son amarillas.",
                "game_type": "color_mixer",
                "levels": 4,
                "tools": ["Paleta de mezclas", "Selector de tonos", "Juego de correspondencias"],
                "quiz": [
                    {"q": "¿Qué colores son primarios?", "a": ["Verde, Naranja, Violeta", "Rojo, Azul, Amarillo", "Negro, Blanco, Gris", "Rosa, Celeste, Lila"], "c": 1},
                    {"q": "¿Qué obtienes mezclando azul y amarillo?", "a": ["Rojo", "Naranja", "Verde", "Violeta"], "c": 2}
                ]
            }
        },
        "pattern_hunter": {
            "icon": "SEARCH",
            "alpha": {
                "title": "Cazador de Patrones",
                "intro": "Identifica secuencias, completa series lógicas y encuentra el intruso en grupos de elementos.",
                "architecture": "El sistema genera patrones basados en formas, colores y números. Debes identificar la regla que gobierna cada secuencia.",
                "security": "Tómate tu tiempo para observar. No hay prisa en resolver los patrones.",
                "challenge": "Encuentra el patrón oculto en 30 segundos o menos.",
                "fact": "Los patrones están en todas partes: en la naturaleza, la música, las matemáticas y el arte.",
                "game_type": "pattern_recognition",
                "levels": 6,
                "tools": ["Secuenciador lógico", "Buscador de anomalías", "Completador de series"],
                "quiz": [
                    {"q": "¿Qué es una secuencia?", "a": ["Un tipo de canción", "Un orden de elementos que sigue una regla", "Un animal prehistórico", "Un tipo de comida"], "c": 1}
                ]
            }
        },
        "drag_drop_builder": {
            "icon": "CONSTRUCTION",
            "alpha": {
                "title": "Constructor Espacial",
                "intro": "Arrastra y suelta bloques para construir estructuras, naves y paisajes espaciales.",
                "architecture": "Usa bloques de diferentes formas y colores. Cada pieza encaja con otras para crear estructuras estables.",
                "security": "Planifica antes de construir. Una buena base hace que tu estructura sea más fuerte.",
                "challenge": "Construye una nave espacial usando al menos 15 piezas diferentes.",
                "fact": "Los arquitectos y ingenieros usan bloques virtuales para planificar edificios reales antes de construirlos.",
                "game_type": "drag_drop",
                "levels": 5,
                "tools": ["Biblioteca de bloques", "Editor de escenarios", "Galería de diseños"],
                "quiz": [
                    {"q": "¿Cuántas piezas mínimo necesitas para la nave?", "a": ["5", "10", "15", "20"], "c": 2}
                ]
            }
        },
        "speed_clicker": {
            "icon": "TOUCH_APP",
            "alpha": {
                "title": "Reflejos de Comandante",
                "intro": "Entrena tu velocidad de reacción tocando objetos que aparecen en pantalla antes de que desaparezcan.",
                "architecture": "Los objetos aparecen en posiciones aleatorias. Debes coordinar tus ojos y manos para ser rápido y preciso.",
                "security": "Mantén la calma y respira. La tensión muscular ralentiza tus reflejos.",
                "challenge": "Toca 20 objetos en menos de 10 segundos.",
                "fact": "Los pilotos de aviones de combate entrenan sus reflejos para reaccionar en menos de 200 milisegundos.",
                "game_type": "reaction_time",
                "levels": 5,
                "tools": ["Medidor de reflejos", "Contador de precisión", "Gráfico de velocidad"],
                "quiz": [
                    {"q": "¿Cuántos objetos debes tocar en el desafío?", "a": ["10", "15", "20", "30"], "c": 2}
                ]
            }
        },
        "puzzle_pieces": {
            "icon": "EXTENSION",
            "alpha": {
                "title": "Rompecabezas Deslizantes",
                "intro": "Ordena piezas deslizantes para formar una imagen completa. Desde puzzles simples hasta desafíos complejos.",
                "architecture": "Las piezas se mueven en un tablero cuadriculado. Solo hay un espacio vacío para mover las piezas adyacentes.",
                "security": "Planifica tus movimientos. A veces es mejor retroceder un paso para avanzar dos.",
                "challenge": "Completa un puzzle de 4x4 en menos de 50 movimientos.",
                "fact": "El rompecabezas del 15 (4x4) fue inventado en 1874 y sigue siendo popular hoy en día.",
                "game_type": "sliding_puzzle",
                "levels": 5,
                "tools": ["Tablero deslizante", "Contador de movimientos", "Vista previa de imagen"],
                "quiz": [
                    {"q": "¿Cuántos espacios vacíos hay?", "a": ["Ninguno", "Uno", "Dos", "Tres"], "c": 1},
                    {"q": "¿En qué año se inventó el puzzle del 15?", "a": ["1800", "1874", "1900", "1950"], "c": 1}
                ]
            }
        },
        "music_maker": {
            "icon": "MUSIC_NOTE",
            "alpha": {
                "title": "Creador Musical",
                "intro": "Crea melodías simples con notas musicales. Aprende ritmo, tempo y escala pentatónica de forma divertida.",
                "architecture": "Coloca notas en una secuencia temporal. Cada nota tiene un sonido diferente y duración específica.",
                "security": "Guarda tus composiciones favoritas. Compártelas con amigos y familia.",
                "challenge": "Crea una melodía de 8 compases usando al menos 5 notas diferentes.",
                "fact": "Mozart comenzó a componer música a los 5 años. La música estimula ambos hemisferios del cerebro.",
                "game_type": "music_sequencer",
                "levels": 4,
                "tools": ["Secuenciador de notas", "Reproductor de melodías", "Biblioteca de instrumentos"],
                "quiz": [
                    {"q": "¿A qué edad comenzó Mozart a componer?", "a": ["3 años", "5 años", "10 años", "15 años"], "c": 1},
                    {"q": "¿Qué estimula la música en el cerebro?", "a": ["Un hemisferio", "Ambos hemisferios", "Ninguno", "Solo el corazón"], "c": 1}
                ]
            }
        },
        "emotions_game": {
            "icon": "EMOJI_EMOTIONS",
            "alpha": {
                "title": "Juego de Emociones",
                "intro": "Aprende a reconocer emociones en rostros. Identifica felicidad, tristeza, enojo, sorpresa y más.",
                "architecture": "Observa expresiones faciales y selecciona la emoción correcta. El juego incluye situaciones sociales.",
                "security": "Todas las emociones son válidas. Es importante reconocer cómo se sienten los demás.",
                "challenge": "Identifica 15 emociones diferentes correctamente.",
                "fact": "Las personas pueden reconocer más de 10,000 expresiones faciales diferentes. La empatía es una habilidad clave.",
                "game_type": "emotion_recognition",
                "levels": 3,
                "tools": ["Galería de rostros", "Selector de emociones", "Escenarios sociales"],
                "quiz": [
                    {"q": "¿Cuántas expresiones pueden reconocer las personas?", "a": ["100", "1000", "10000", "100000"], "c": 2},
                    {"q": "¿Qué habilidad se desarrolla con este juego?", "a": ["Fuerza", "Empatía", "Velocidad", "Memoria"], "c": 1}
                ]
            }
        },
        "basic_math_adventure": {
            "icon": "LOOKS_TWO",
            "alpha": {
                "title": "Aventura de Matemáticas",
                "intro": "Aprende sumas y restas jugando. Ayuda a personajes a contar objetos, repartir cosas equitativamente y resolver problemas.",
                "architecture": "Cada nivel presenta un problema matemático contextualizado en una historia. El niño selecciona la respuesta correcta.",
                "security": "No hay respuestas incorrectas malas, solo oportunidades de aprender. Anima a intentar de nuevo.",
                "challenge": "Resuelve 20 problemas de suma y resta sin errores.",
                "fact": "Los niños que juegan con matemáticas desde pequeños desarrollan mejor el pensamiento lógico.",
                "game_type": "math_basic",
                "levels": 5,
                "tools": ["Contador visual", "Línea numérica", "Bloques de conteo"],
                "quiz": [
                    {"q": "¿Cuánto es 5 + 3?", "a": ["7", "8", "9", "6"], "c": 1},
                    {"q": "¿Cuánto es 10 - 4?", "a": ["5", "6", "7", "4"], "c": 1}
                ]
            }
        },
        "animal_world": {
            "icon": "PETS",
            "alpha": {
                "title": "Mundo Animal",
                "intro": "Conoce animales de todo el mundo: mamíferos, aves, reptiles, peces. Aprende qué comen, dónde viven y sonidos.",
                "architecture": "Cada animal tiene una ficha con información, sonido y curiosidades. Juegos de emparejamiento de animales con hábitats.",
                "security": "Todos los animales son importantes en la naturaleza. Respetamos y cuidamos a los animales.",
                "challenge": "Identifica 20 animales diferentes y sus hábitats correctamente.",
                "fact": "Hay más de 8.7 millones de especies de animales en el planeta Tierra.",
                "game_type": "animal_learning",
                "levels": 4,
                "tools": ["Enciclopedia animal", "Reproductor de sonidos", "Mapa de hábitats"],
                "quiz": [
                    {"q": "¿Cuántas especies de animales existen?", "a": ["100 mil", "1 millón", "8.7 millones", "100 millones"], "c": 2},
                    {"q": "¿Qué debemos hacer con los animales?", "a": ["Cazarlos", "Respetarlos", "Ignorarlos", "Molestarlos"], "c": 1}
                ]
            }
        },
        "drawing_canvas": {
            "icon": "BRUSH",
            "alpha": {
                "title": "Lienzo Creativo",
                "intro": "Dibuja, pinta y crea arte digital. Pinceles, colores, formas y sellos para expresar tu creatividad.",
                "architecture": "Lienzo digital con herramientas de dibujo. Guarda tus obras y compártelas.",
                "security": "Tu arte es único. No compares tu creatividad con la de otros. Todos somos artistas.",
                "challenge": "Crea un dibujo usando al menos 5 colores diferentes y 3 formas.",
                "fact": "Pablo Picasso dijo: 'Todos los niños nacen artistas'. La creatividad no tiene límites.",
                "game_type": "digital_art",
                "levels": 3,
                "tools": ["Pincel mágico", "Paleta de colores", "Formas geométricas", "Galería personal"],
                "quiz": [
                    {"q": "¿Qué dijo Picasso sobre los niños?", "a": ["Son tontos", "Son artistas", "Son lentos", "Son genios"], "c": 1},
                    {"q": "¿Cuántos colores debes usar en el desafío?", "a": ["3", "5", "10", "2"], "c": 1}
                ]
            }
        },
        "shape_sorter": {
            "icon": "CATEGORY",
            "alpha": {
                "title": "Clasificador de Formas",
                "intro": "Ordena formas geométricas por color, tamaño y tipo. Aprende círculos, cuadrados, triángulos y más.",
                "architecture": "Las formas caen desde arriba. Arrástralas a los contenedores correctos según su categoría.",
                "security": "Observa cuidadosamente antes de soltar. Algunas formas pueden parecerse mucho.",
                "challenge": "Clasifica 50 formas en menos de 2 minutos sin errores.",
                "fact": "Las formas geométricas están en todas partes: las señales de tráfico, los edificios, las ventanas.",
                "game_type": "shape_classifier",
                "levels": 4,
                "tools": ["Contenedores de formas", "Cinta transportadora", "Contador de precisión"],
                "quiz": [
                    {"q": "¿Cuántos lados tiene un triángulo?", "a": ["2", "3", "4", "5"], "c": 1},
                    {"q": "¿Qué forma tiene una pelota?", "a": ["Cuadrado", "Triángulo", "Círculo", "Rectángulo"], "c": 2}
                ]
            }
        },
        "nature_explorer": {
            "icon": "FOREST",
            "alpha": {
                "title": "Explorador de la Naturaleza",
                "intro": "Descubre plantas, flores, árboles e insectos. Aprende cómo crecen los seres vivos y sus ciclos de vida.",
                "architecture": "Explora diferentes ecosistemas. Cada planta o animal tiene información sobre su ciclo de vida.",
                "security": "Trata la naturaleza con respeto. No debemos dañar plantas ni animales en la vida real.",
                "challenge": "Completa el ciclo de vida de una mariposa en orden correcto.",
                "fact": "Las mariposas comienzan como orugas, luego hacen capullo y finalmente salen alas hermosas.",
                "game_type": "nature_discovery",
                "levels": 3,
                "tools": ["Lupa virtual", "Colección de especímenes", "Diario de observaciones"],
                "quiz": [
                    {"q": "¿En qué se convierte una oruga?", "a": ["Ave", "Mariposa", "Pez", "Rana"], "c": 1},
                    {"q": "¿Cómo debemos tratar la naturaleza?", "a": ["Con respeto", "Dañándola", "Ignorándola", "Destruyéndola"], "c": 0}
                ]
            }
        },
        "story_creator": {
            "icon": "MENU_BOOK",
            "alpha": {
                "title": "Creador de Cuentos",
                "intro": "Crea tus propias historias eligiendo personajes, escenarios y aventuras. Narrativa interactiva para niños.",
                "architecture": "Selecciona elementos para construir una historia. El sistema genera una narrativa coherente.",
                "security": "Todas las historias son buenas. No hay ideas tontas, solo creatividad sin límites.",
                "challenge": "Crea una historia con 3 personajes, 2 escenarios y un final feliz.",
                "fact": "Los cuentos ayudan a desarrollar el lenguaje y la imaginación desde edades tempranas.",
                "game_type": "story_builder",
                "levels": 4,
                "tools": ["Galería de personajes", "Selector de escenarios", "Constructor de tramas", "Lector de historias"],
                "quiz": [
                    {"q": "¿Cuántos personajes necesitas?", "a": ["1", "2", "3", "5"], "c": 2},
                    {"q": "¿Qué desarrollan los cuentos?", "a": ["Fuerza física", "Lenguaje e imaginación", "Velocidad", "Sueño"], "c": 1}
                ]
            }
        },
        "shadow_matching": {
            "icon": "CONTENT_COPY",
            "alpha": {
                "title": "Encuentra la Sombra",
                "intro": "Relaciona objetos con sus sombras correspondientes. Desarrolla percepción visual y pensamiento espacial.",
                "architecture": "Se muestra un objeto y varias sombras. El niño debe seleccionar cuál sombra corresponde al objeto.",
                "security": "Observa la forma cuidadosamente. Algunas sombras pueden parecerse pero tienen detalles diferentes.",
                "challenge": "Encuentra 20 parejas objeto-sombra correctamente.",
                "fact": "Las sombras cambian según la posición de la luz. Esto nos ayuda a entender el espacio tridimensional.",
                "game_type": "shadow_match",
                "levels": 4,
                "tools": ["Proyector de sombras", "Galería de objetos", "Rotador de luz"],
                "quiz": [
                    {"q": "¿Qué hace cambiar las sombras?", "a": ["El color", "La posición de la luz", "El sonido", "El tacto"], "c": 1},
                    {"q": "¿Qué desarrolla este juego?", "a": ["Fuerza", "Percepción espacial", "Oído", "Gusto"], "c": 1}
                ]
            }
        },
        "size_sorting": {
            "icon": "SORT",
            "alpha": {
                "title": "Ordena por Tamaño",
                "intro": "Organiza objetos del más pequeño al más grande o viceversa. Conceptos de ordenación y comparación.",
                "architecture": "Arrastra objetos para ordenarlos según su tamaño. Compara objetos relacionados como frutas, animales, juguetes.",
                "security": "Compara cuidadosamente. Algunos objetos pueden tener tamaños similares.",
                "challenge": "Ordena 10 objetos de menor a mayor sin errores.",
                "fact": "Los elefantes africanos son los animales terrestres más grandes, pueden pesar hasta 6,000 kg.",
                "game_type": "size_sort",
                "levels": 5,
                "tools": ["Escala de comparación", "Medidor visual", "Contador de objetos"],
                "quiz": [
                    {"q": "¿Qué animal terrestre es más grande?", "a": ["Jirafa", "Elefante africano", "Rinoceronte", "Hipopótamo"], "c": 1},
                    {"q": "¿Cuántos objetos ordenas en el desafío?", "a": ["5", "8", "10", "15"], "c": 2}
                ]
            }
        },
        "sound_matching": {
            "icon": "HEARING",
            "alpha": {
                "title": "Adivina el Sonido",
                "intro": "Escucha sonidos de animales, instrumentos, vehículos y objetos cotidianos. Identifica qué lo produce.",
                "architecture": "Reproduce un sonido y muestra varias imágenes. El niño selecciona la imagen que corresponde al sonido.",
                "security": "Escucha atentamente. Cierra los ojos si es necesario para concentrarte mejor.",
                "challenge": "Identifica 25 sonidos diferentes correctamente.",
                "fact": "Los murciélagos usan la ecolocalización para navegar. Emiten sonidos que rebotan en los objetos.",
                "game_type": "sound_match",
                "levels": 4,
                "tools": ["Biblioteca de sonidos", "Ecualizador visual", "Selector de categorías"],
                "quiz": [
                    {"q": "¿Qué usan los murciélagos para navegar?", "a": ["Luz", "Ecolocalización", "Olfato", "Tacto"], "c": 1},
                    {"q": "¿Cuántos sonidos debes identificar?", "a": ["10", "15", "25", "30"], "c": 2}
                ]
            }
        },
        "mirror_drawing": {
            "icon": "FLIP",
            "alpha": {
                "title": "Dibuja al Espejo",
                "intro": "Completa dibujos simétricos. Dibuja la mitad faltante para crear imágenes simétricas perfectas.",
                "architecture": "Muestra la mitad de una imagen. El niño dibuja la mitad faltante reflejando la primera parte.",
                "security": "Observa los detalles de la mitad mostrada. La simetría requiere precisión y paciencia.",
                "challenge": "Completa 5 dibujos simétricos con 90% de precisión.",
                "fact": "Las mariposas tienen alas simétricas perfectas. La simetría existe en toda la naturaleza.",
                "game_type": "symmetry_drawing",
                "levels": 4,
                "tools": ["Línea de simetría", "Pincel de espejo", "Borrador de precisión", "Galería de plantillas"],
                "quiz": [
                    {"q": "¿Qué insecto tiene alas simétricas?", "a": ["Mosca", "Mariposa", "Abeja", "Araña"], "c": 1},
                    {"q": "¿Cuántos dibujos completas en el desafío?", "a": ["3", "5", "8", "10"], "c": 1}
                ]
            }
        },
        "telling_time": {
            "icon": "ACCESS_TIME",
            "alpha": {
                "title": "Aprende la Hora",
                "intro": "Lee relojes analógicos y digitales. Aprende horas, medias horas, cuartos de hora.",
                "architecture": "Relojes interactivos que muestran diferentes horas. El niño selecciona la hora correcta.",
                "security": "El tiempo es importante. Nos ayuda a organizar nuestras actividades diarias.",
                "challenge": "Lee correctamente 20 relojes diferentes.",
                "fact": "Los relojes mecánicos fueron inventados en Europa en el siglo XIV. Antes se usaban relojes de sol.",
                "game_type": "time_learning",
                "levels": 5,
                "tools": ["Reloj analógico", "Reloj digital", "Conversor de formato", "Planificador de tiempo"],
                "quiz": [
                    {"q": "¿Cuándo se inventaron los relojes mecánicos?", "a": ["Siglo X", "Siglo XIV", "Siglo XVIII", "Siglo XX"], "c": 1},
                    {"q": "¿Qué tipo de reloj usaban antes?", "a": ["Reloj de pulsera", "Reloj de sol", "Reloj digital", "Reloj inteligente"], "c": 1}
                ]
            }
        },
        "body_parts": {
            "icon": "ACCESSIBILITY",
            "alpha": {
                "title": "Conoce tu Cuerpo",
                "intro": "Aprende partes del cuerpo humano, órganos y sistemas. Anatomía básica para niños.",
                "architecture": "Modelo interactivo del cuerpo humano. Toca diferentes partes para aprender sus nombres y funciones.",
                "security": "Tu cuerpo es importante y único. Cuida tu salud con buena alimentación y ejercicio.",
                "challenge": "Identifica 15 partes del cuerpo y sus funciones básicas.",
                "fact": "El corazón late aproximadamente 100,000 veces al día. Bombear sangre a todo el cuerpo.",
                "game_type": "anatomy_learning",
                "levels": 3,
                "tools": ["Cuerpo interactivo", "Ampliador de órganos", "Sistema esquelético", "Sistema muscular"],
                "quiz": [
                    {"q": "¿Cuántas veces late el corazón al día?", "a": ["10,000", "50,000", "100,000", "500,000"], "c": 2},
                    {"q": "¿Qué bombea el corazón?", "a": ["Aire", "Sangre", "Agua", "Comida"], "c": 1}
                ]
            }
        },
        
        # ─── PROTOCOLO DELTA: Simuladores y Herramientas ───
        "terminal_simulator": {
            "icon": "TERMINAL",
            "delta": {
                "title": "Simulador de Terminal",
                "intro": "Aprende comandos básicos de terminal en un entorno seguro: listar archivos, crear carpetas, navegar directorios.",
                "architecture": "El terminal interpreta comandos de texto y ejecuta operaciones en el sistema de archivos virtual. Cada comando tiene una función específica.",
                "security": "Verifica siempre el directorio actual antes de ejecutar comandos. Usa 'pwd' para saber dónde estás.",
                "challenge": "Completa 10 operaciones de archivo sin usar el ratón.",
                "fact": "Los hackers de películas usan terminales, pero en realidad son herramientas cotidianas para administradores de sistemas.",
                "game_type": "terminal",
                "levels": 8,
                "tools": ["Editor de comandos", "Visualizador de directorios", "Historial de operaciones"],
                "commands": ["ls", "cd", "mkdir", "pwd", "clear", "help"],
                "quiz": [
                    {"q": "¿Qué comando lista archivos?", "a": ["cd", "ls", "mkdir", "clear"], "c": 1},
                    {"q": "¿Qué hace 'mkdir'?", "a": ["Borra archivos", "Lista contenido", "Crea carpetas", "Navega directorios"], "c": 2}
                ]
            }
        },
        "network_mapper": {
            "icon": "ACCOUNT_TREE",
            "delta": {
                "title": "Mapa de Red Interactivo",
                "intro": "Diseña topologías de red: conecta routers, switches y endpoints. Simula el flujo de datos.",
                "architecture": "Los paquetes de datos viajan de origen a destino saltando entre nodos. Cada dispositivo procesa y reenvía la información.",
                "security": "Nunca conectes dispositivos desconocidos a tu red. Podrían ser puntos de acceso para intrusos.",
                "challenge": "Crea una red con 5 nodos que se comuniquen entre sí.",
                "fact": "Internet es una red de redes. Millones de dispositivos se conectan diariamente para enviar correos, videos y mensajes.",
                "game_type": "network_designer",
                "levels": 6,
                "tools": ["Arrastrar y soltar nodos", "Simulador de paquetes", "Probador de conectividad"],
                "quiz": [
                    {"q": "¿Qué dispositivo conecta diferentes redes?", "a": ["Switch", "Router", "Cables", "Monitor"], "c": 1},
                    {"q": "¿Qué es un paquete de datos?", "a": ["Un sobre físico", "Una unidad de información enviada por red", "Un tipo de comida", "Un archivo grande"], "c": 1}
                ]
            }
        },
        "code_breaker": {
            "icon": "CODE",
            "delta": {
                "title": "Descifrador de Códigos",
                "intro": "Resuelve cifrados simples: César, sustitución y binario básico. Ideal para iniciarse en criptografía.",
                "architecture": "Los cifrados transforman texto legible en código. La clave determina cómo se codifica y decodifica el mensaje.",
                "security": "Nunca uses cifrados simples para información importante. Son fáciles de romper con computadoras modernas.",
                "challenge": "Descifra 5 mensajes codificados antes de que termine el tiempo.",
                "fact": "Julio César usaba este cifrado para enviar mensajes secretos a sus generales en el siglo I a.C.",
                "game_type": "crypto_puzzle",
                "levels": 7,
                "tools": ["Decodificador César", "Conversor binario", "Analizador de frecuencia"],
                "quiz": [
                    {"q": "¿Qué es el cifrado César?", "a": ["Un tipo de comida", "Desplazamiento de letras", "Un virus informático", "Un lenguaje de programación"], "c": 1},
                    {"q": "¿Cuántos bits tiene un byte?", "a": ["4", "8", "16", "32"], "c": 1}
                ]
            }
        },
        "logic_gates": {
            "icon": "DEVELOPER_BOARD",
            "delta": {
                "title": "Puertas Lógicas Interactivas",
                "intro": "Construye circuitos con AND, OR, NOT, XOR. Visualiza cómo fluye la electricidad según las entradas.",
                "architecture": "Las puertas lógicas son bloques básicos de la computación. Combinándolas se pueden crear circuitos complejos.",
                "security": "Los circuitos mal diseñados pueden causar cortocircuitos. Siempre verifica las conexiones antes de encender.",
                "challenge": "Construye un circuito que encienda una luz solo si ambos interruptores están activos.",
                "fact": "Las computadoras modernas contienen miles de millones de transistores que funcionan como puertas lógicas.",
                "game_type": "circuit_builder",
                "levels": 5,
                "tools": ["Biblioteca de compuertas", "Simulador eléctrico", "Probador de estados"],
                "quiz": [
                    {"q": "¿Qué puerta lógica necesita ambas entradas en 1 para salir 1?", "a": ["OR", "AND", "NOT", "XOR"], "c": 1},
                    {"q": "¿Qué hace la puerta NOT?", "a": ["Suma entradas", "Invierte la entrada", "Multiplica valores", "Divide señales"], "c": 1}
                ]
            }
        },
        "file_manager": {
            "icon": "FOLDER",
            "delta": {
                "title": "Administrador de Archivos",
                "intro": "Organiza archivos, crea carpetas, renombra documentos y entiende extensiones de archivo comunes.",
                "architecture": "Los sistemas de archivos organizan datos jerárquicamente. Las extensiones indican el tipo de contenido.",
                "security": "Nunca abras archivos con extensiones sospechosas (.exe, .bat) de fuentes desconocidas.",
                "challenge": "Organiza 30 archivos en 5 categorías diferentes en menos de 2 minutos.",
                "fact": "El primer sistema de archivos fue creado en 1965 para mainframes IBM.",
                "game_type": "file_organizer",
                "levels": 6,
                "tools": ["Explorador de carpetas", "Clasificador automático", "Buscador de duplicados"],
                "quiz": [
                    {"q": "¿Qué extensión tienen los documentos de texto?", "a": [".jpg", ".txt", ".exe", ".mp3"], "c": 1},
                    {"q": "¿Qué es una carpeta?", "a": ["Un tipo de archivo", "Un contenedor para organizar archivos", "Un virus", "Un programa"], "c": 1}
                ]
            }
        },
        "password_builder": {
            "icon": "LOCK",
            "delta": {
                "title": "Constructor de Contraseñas Seguras",
                "intro": "Aprende a crear contraseñas fuertes, usa generadores aleatorios y comprende la entropía de seguridad.",
                "architecture": "Una contraseña segura debe tener longitud, complejidad y aleatoriedad. La entropía mide su resistencia a ataques.",
                "security": "Nunca reutilices contraseñas. Usa un gestor de contraseñas para mantenerlas seguras.",
                "challenge": "Crea una contraseña con 100% de fuerza según el medidor.",
                "fact": "Una contraseña de 8 caracteres puede romperse en minutos, pero una de 12 lleva siglos.",
                "game_type": "password_game",
                "levels": 5,
                "tools": ["Generador aleatorio", "Medidor de fuerza", "Comprobador de patrones"],
                "quiz": [
                    {"q": "¿Qué hace una contraseña más segura?", "a": ["Usar solo números", "Combinar letras, números y símbolos", "Ser corta", "Usar tu nombre"], "c": 1},
                    {"q": "¿Qué es la entropía de contraseña?", "a": ["Una medida de aleatoriedad y seguridad", "Un virus", "Un tipo de archivo", "Un programa hacker"], "c": 0}
                ]
            }
        },
        "hangman_game": {
            "icon": "SPORTS_SCOREBOARD",
            "delta": {
                "title": "Ahorcado Educativo",
                "intro": "Adivina la palabra oculta letra por letra. Categorías: ciencia, tecnología, historia, geografía.",
                "architecture": "Una palabra secreta se oculta con guiones. Adivina letras para revelarla antes de que se complete el dibujo.",
                "security": "Empieza con las vocales más comunes. Analiza la longitud de la palabra para deducir posibilidades.",
                "challenge": "Adivina la palabra sin cometer más de 3 errores.",
                "fact": "El ahorcado se juega desde el siglo XIX. Es excelente para practicar ortografía y vocabulario.",
                "game_type": "hangman",
                "levels": 6,
                "tools": ["Tablero de letras", "Dibujo progresivo", "Pista de categoría"],
                "quiz": [
                    {"q": "¿Cómo se muestra la palabra oculta?", "a": ["Con asteriscos", "Con guiones", "Con puntos", "Con números"], "c": 1},
                    {"q": "¿Desde cuándo se juega el ahorcado?", "a": ["Siglo XVIII", "Siglo XIX", "Siglo XX", "Siglo XXI"], "c": 1}
                ]
            }
        },
        "typing_race": {
            "icon": "KEYBOARD",
            "delta": {
                "title": "Carrera de Mecanografía",
                "intro": "Mejora tu velocidad de escritura. Practica con palabras, frases y párrafos de dificultad creciente.",
                "architecture": "Las palabras aparecen en pantalla. Escribir correctamente avanza tu personaje en la carrera.",
                "security": "Mantén los dedos en la fila base (ASDF JKLÑ). No mires el teclado, mira la pantalla.",
                "challenge": "Escribe 60 palabras por minuto con 95% de precisión.",
                "fact": "La mecanografía rápida puede ahorrar horas de trabajo cada semana. La velocidad promedio es de 40 PPM.",
                "game_type": "typing_race",
                "levels": 8,
                "tools": ["Medidor de PPM", "Teclado virtual", "Análisis de precisión", "Progresión de dificultad"],
                "quiz": [
                    {"q": "¿Dónde deben estar los dedos base?", "a": ["QWERT", "ASDF JKLÑ", "ZXCV", "12345"], "c": 1},
                    {"q": "¿Cuál es la velocidad promedio de escritura?", "a": ["20 PPM", "40 PPM", "80 PPM", "120 PPM"], "c": 1}
                ]
            }
        },
        "virtual_laboratory": {
            "icon": "SCIENCE",
            "delta": {
                "title": "Laboratorio Virtual",
                "intro": "Experimentos científicos virtuales: química, física, biología. Seguro, económico y sin riesgos.",
                "architecture": "Simula reacciones químicas, experimentos de física y observaciones biológicas con equipos virtuales.",
                "security": "Aunque es virtual, sigue protocolos de laboratorio. Documenta todos tus experimentos.",
                "challenge": "Realiza 5 experimentos de química sin errores de medición.",
                "fact": "Marie Curie fue la primera mujer en ganar un Nobel y la única en ganar dos en diferentes ciencias.",
                "game_type": "virtual_lab",
                "levels": 5,
                "tools": ["Matraz virtual", "Microscopio digital", "Balanzas de precisión", "Cuaderno de laboratorio"],
                "quiz": [
                    {"q": "¿Qué tipo de experimentos puedes hacer?", "a": ["Solo química", "Química, física, biología", "Solo física", "Solo biología"], "c": 1},
                    {"q": "¿Quién fue Marie Curie?", "a": ["Primera mujer Nobel", "Astronauta", "Pintora", "Escritora"], "c": 0}
                ]
            }
        },
        "geo_explorer": {
            "icon": "PUBLIC",
            "delta": {
                "title": "Explorador Geográfico",
                "intro": "Aprende geografía mundial: países, capitales, banderas, continentes y monumentos famosos.",
                "architecture": "Mapa interactivo del mundo. Selecciona países para aprender sobre su cultura, ubicación y datos curiosos.",
                "security": "Todos los países merecen respeto. Aprendemos sobre diversidad cultural y respetamos diferencias.",
                "challenge": "Identifica 30 países en el mapa mundi con sus capitales.",
                "fact": "Hay 195 países reconocidos en el mundo hoy en día. Rusia es el país más grande.",
                "game_type": "geography_learning",
                "levels": 6,
                "tools": ["Mapa mundi interactivo", "Buscador de capitales", "Galería de banderas", "Quiz de monumentos"],
                "quiz": [
                    {"q": "¿Cuántos países hay en el mundo?", "a": ["150", "195", "200", "250"], "c": 1},
                    {"q": "¿Cuál es el país más grande?", "a": ["China", "Estados Unidos", "Rusia", "Canadá"], "c": 2}
                ]
            }
        },
        "historical_timeline": {
            "icon": "HISTORY",
            "delta": {
                "title": "Línea del Tiempo Histórica",
                "intro": "Viaja por la historia: civilizaciones antiguas, edad media, revoluciones, era moderna y tecnología.",
                "architecture": "Timeline interactivo con eventos históricos. Conecta causas y consecuencias de eventos importantes.",
                "security": "Aprender del pasado nos ayuda a construir un mejor futuro. La historia nos enseña lecciones valiosas.",
                "challenge": "Ordena 20 eventos históricos en la línea del tiempo correctamente.",
                "fact": "La Gran Pirámide de Giza fue construida hace más de 4,500 años y es una de las 7 maravillas del mundo antiguo.",
                "game_type": "history_timeline",
                "levels": 5,
                "tools": ["Navegador de épocas", "Biografías históricas", "Mapas históricos", "Comparador de civilizaciones"],
                "quiz": [
                    {"q": "¿Cuánto hace que se construyó la Gran Pirámide?", "a": ["1,000 años", "2,500 años", "4,500 años", "10,000 años"], "c": 2},
                    {"q": "¿Qué nos enseña la historia?", "a": ["Nada", "Lecciones valiosas", "Solo fechas", "Solo nombres"], "c": 1}
                ]
            }
        },
        "creative_writing": {
            "icon": "EDIT_NOTE",
            "delta": {
                "title": "Escritura Creativa",
                "intro": "Escribe historias, poesía y ensayos. Aprende estructura narrativa, vocabulario y técnicas de escritura.",
                "architecture": "Editor de texto con prompts creativos. Guarda borradores y publica tus mejores obras.",
                "security": "Tu voz es única. No copies el trabajo de otros. La originalidad es valiosa.",
                "challenge": "Escribe una historia corta de 500 palabras con inicio, desarrollo y final.",
                "fact": "Gabriel García Márquez escribió 'Cien años de soledad' y ganó el Nobel de Literatura en 1982.",
                "game_type": "writing_workshop",
                "levels": 4,
                "tools": ["Editor de textos", "Diccionario de sinónimos", "Corrector ortográfico", "Biblioteca de prompts"],
                "quiz": [
                    {"q": "¿Quién escribió 'Cien años de soledad'?", "a": ["Pablo Neruda", "Gabriel García Márquez", "Mario Vargas Llosa", "Jorge Luis Borges"], "c": 1},
                    {"q": "¿Cuántas palabras debe tener tu historia?", "a": ["100", "500", "1000", "2000"], "c": 1}
                ]
            }
        },
        "mental_math": {
            "icon": "SPEED",
            "delta": {
                "title": "Cálculo Mental Rápido",
                "intro": "Ejercita tu cerebro con operaciones matemáticas rápidas. Multiplicación, división, potencias y raíces.",
                "architecture": "Problemas de dificultad progresiva. Temporizador para medir velocidad. Racha de respuestas correctas.",
                "security": "No uses calculadora. Entrena tu mente. El cálculo mental mejora la concentración y memoria.",
                "challenge": "Resuelve 50 operaciones en 2 minutos con 90% de precisión.",
                "fact": "Los matemáticos indios antiguos podían multiplicar números grandes mentalmente gracias a técnicas de Vedic math.",
                "game_type": "mental_math",
                "levels": 7,
                "tools": ["Generador de problemas", "Temporizador", "Contador de racha", "Ranking de velocidad"],
                "quiz": [
                    {"q": "¿Qué mejora el cálculo mental?", "a": ["Solo fuerza", "Concentración y memoria", "Solo velocidad", "Sueño"], "c": 1},
                    {"q": "¿Cuántas operaciones en el desafío?", "a": ["10", "25", "50", "100"], "c": 2}
                ]
            }
        },
        "basic_physics": {
            "icon": "PHYSICS",
            "delta": {
                "title": "Física Básica Interactiva",
                "intro": "Experimenta con gravedad, fricción, energía y movimiento. Simulaciones de física Newtoniana.",
                "architecture": "Sandbox de física 2D. Coloca objetos, aplica fuerzas y observa el comportamiento.",
                "security": "La física tiene leyes inmutables. Experimenta libremente, los resultados son predecibles.",
                "challenge": "Construye una máquina de Rube Goldberg que funcione usando 5 objetos.",
                "fact": "Isaac Newton describió la gravedad en 1687. Una manzana inspiró su teoría sobre fuerzas.",
                "game_type": "physics_simulator",
                "levels": 5,
                "tools": ["Sandbox de física", "Generador de objetos", "Medidor de fuerzas", "Creador de pendientes"],
                "quiz": [
                    {"q": "¿Quién describió la gravedad?", "a": ["Einstein", "Newton", "Galileo", "Tesla"], "c": 1},
                    {"q": "¿Qué inspiró a Newton?", "a": ["Una manzana", "Una pera", "Una naranja", "Una uva"], "c": 0}
                ]
            }
        },
        "astronomy_explorer": {
            "icon": "NIGHTLIGHT_ROUNDED",
            "delta": {
                "title": "Explorador Astronómico",
                "intro": "Viaja por el sistema solar y más allá. Planetas, estrellas, galaxias y fenómenos cósmicos.",
                "architecture": "Visualización 3D del espacio. Navega entre planetas, observa órbitas y escala del universo.",
                "security": "El espacio es vasto y misterioso. Respeta la fragilidad de nuestro planeta en el cosmos.",
                "challenge": "Identifica los 8 planetas del sistema solar en orden y sus características principales.",
                "fact": "La luz del Sol tarda 8 minutos en llegar a la Tierra. Vemos el Sol como era hace 8 minutos.",
                "game_type": "space_explorer",
                "levels": 6,
                "tools": ["Telescopio virtual", "Navegador planetario", "Simulador de órbitas", "Catálogo estelar"],
                "quiz": [
                    {"q": "¿Cuántos planetas hay en el sistema solar?", "a": ["7", "8", "9", "10"], "c": 1},
                    {"q": "¿Cuánto tarda la luz del Sol?", "a": ["1 segundo", "8 minutos", "1 hora", "1 día"], "c": 1}
                ]
            }
        },
        
        # ─── PROTOCOLO OMEGA: Herramientas Avanzadas y Labs ───
        "pentest_lab": {
            "icon": "SECURITY",
            "omega": {
                "title": "Laboratorio de Pentesting Ético",
                "intro": "Entorno sandbox para practicar análisis de vulnerabilidades, escaneo de puertos y enumeración de servicios.",
                "architecture": "El pentesting sigue metodologías definidas: reconocimiento, escaneo, explotación y reporte. Cada fase tiene herramientas específicas.",
                "security": "Solo realiza pentesting en sistemas donde tengas autorización explícita por escrito.",
                "challenge": "Encuentra 3 vulnerabilidades críticas en el sistema objetivo.",
                "fact": "El término 'hacker' originalmente significaba alguien curioso que disfrutaba explorando sistemas.",
                "game_type": "pentest_simulator",
                "levels": 10,
                "tools": ["Escáner de puertos Nmap", "Analizador de vulnerabilidades", "Inyector de pruebas", "Reporteador de hallazgos"],
                "quiz": [
                    {"q": "¿Qué es un pentest?", "a": ["Un virus peligroso", "Prueba de penetración autorizada", "Un tipo de firewall", "Un lenguaje de código"], "c": 1},
                    {"q": "¿Qué hace Nmap?", "a": ["Borra archivos", "Escanea redes y puertos", "Diseña páginas web", "Envía correos"], "c": 1}
                ]
            }
        },
        "server_admin": {
            "icon": "DNS",
            "omega": {
                "title": "Administrador de Servidores",
                "intro": "Simula la gestión de servidores Linux: gestión de usuarios, permisos, procesos y logs del sistema.",
                "architecture": "Linux organiza recursos jerárquicamente. El kernel gestiona hardware, mientras el espacio de usuario ejecuta aplicaciones.",
                "security": "Nunca ejecutes comandos como root sin verificar. Un error puede comprometer todo el sistema.",
                "challenge": "Configura un servidor web funcional con múltiples usuarios y permisos correctos.",
                "fact": "Linux corre en el 96.3% de los servidores web del mundo top 1 millón.",
                "game_type": "server_admin",
                "levels": 8,
                "tools": ["Gestor de usuarios", "Editor de permisos", "Monitor de procesos", "Analizador de logs", "Configurador de servicios"],
                "commands": ["useradd", "chmod", "chown", "ps", "top", "systemctl", "journalctl", "nginx"],
                "quiz": [
                    {"q": "¿Qué hace 'chmod 755'?", "a": ["Borra un archivo", "Cambia permisos de lectura, escritura y ejecución", "Crea un usuario", "Instala software"], "c": 1},
                    {"q": "¿Dónde se guardan los logs en Linux?", "a": ["/home", "/var/log", "/tmp", "/root"], "c": 1}
                ]
            }
        },
        "malware_analyzer": {
            "icon": "BUG_REPORT",
            "omega": {
                "title": "Analizador de Malware",
                "intro": "Sandbox seguro para analizar comportamiento de software malicioso: patrones, firmas y técnicas de ofuscación.",
                "architecture": "El análisis dinámico ejecuta malware en entorno controlado. El estático examina el código sin ejecutarlo.",
                "security": "Nunca ejecutes malware fuera de un sandbox aislado. Una infección puede propagarse rápidamente.",
                "challenge": "Identifica el tipo de malware y su vector de infección en 5 minutos.",
                "fact": "El primer virus de computadora se llamó 'Creeper' y se creó en 1971 como experimento.",
                "game_type": "malware_analysis",
                "levels": 7,
                "tools": ["Descompilador", "Analizador de strings", "Monitor de comportamiento", "Detector de firmas"],
                "quiz": [
                    {"q": "¿Qué es un sandbox?", "a": ["Un juego de niños", "Entorno aislado para análisis seguro", "Un tipo de virus", "Un firewall"], "c": 1},
                    {"q": "¿Qué es una firma de malware?", "a": ["Un documento legal", "Patrón único que identifica amenaza", "Un certificado SSL", "Un tipo de cifrado"], "c": 1}
                ]
            }
        },
        "crypto_suite": {
            "icon": "ENHANCED_ENCRYPTION",
            "omega": {
                "title": "Suite de Criptografía Avanzada",
                "intro": "Herramientas de encriptación: AES, RSA, hashing SHA-256, firmas digitales y certificados SSL.",
                "architecture": "La criptografía moderna usa algoritmos matemáticos complejos. La asimétrica usa pares de claves; la simétrica usa una sola clave.",
                "security": "Nunca compartas tu clave privada. Las claves públicas pueden distribuirse libremente.",
                "challenge": "Cifra y descifra un mensaje usando claves públicas y privadas RSA.",
                "fact": "La computación cuántica podría romper RSA en el futuro, por eso se desarrolla criptografía post-cuántica.",
                "game_type": "crypto_tools",
                "levels": 9,
                "tools": ["Generador de claves RSA", "Cifrador AES", "Calculadora de hashes", "Verificador de firmas", "Analizador de certificados"],
                "quiz": [
                    {"q": "¿Qué es la criptografía asimétrica?", "a": ["Usa la misma clave", "Usa par de claves pública y privada", "No usa claves", "Solo usa números primos"], "c": 1},
                    {"q": "¿Qué algoritmo de hash es más seguro?", "a": ["MD5", "SHA-1", "SHA-256", "CRC32"], "c": 2}
                ]
            }
        },
        "incident_response": {
            "icon": "WARNING",
            "omega": {
                "title": "Respuesta a Incidentes",
                "intro": "Simula gestión de incidentes de seguridad: detección, contención, erradicación y recuperación.",
                "architecture": "Los equipos SOC monitorean 24/7. Cuando detectan una amenaza, siguen protocolos establecidos para responder.",
                "security": "Documenta todo durante un incidente. La evidencia digital es crucial para investigaciones posteriores.",
                "challenge": "Contiene una brecha de seguridad activa en menos de 10 minutos de simulación.",
                "fact": "El tiempo promedio para detectar una brecha de seguridad es de 280 días.",
                "game_type": "incident_simulator",
                "levels": 6,
                "tools": ["Detector de intrusiones", "Aislador de sistemas", "Analizador forense", "Generador de reportes"],
                "quiz": [
                    {"q": "¿Cuáles son las fases de respuesta a incidentes?", "a": ["Detección, Contención, Erradicación, Recuperación", "Ataque, Defensa, Victoria", "Copiar, Pegar, Borrar", "Inicio, Proceso, Fin"], "c": 0},
                    {"q": "¿Qué es la contención?", "a": ["Eliminar el malware", "Limitar el daño y propagación", "Recuperar datos", "Documentar el incidente"], "c": 1}
                ]
            }
        },
        "network_analyzer": {
            "icon": "NETWORK_CHECK",
            "omega": {
                "title": "Analizador de Tráfico de Red",
                "intro": "Captura y analiza paquetes de red: protocolos HTTP, DNS, TCP. Identifica anomalías y tráfico sospechoso.",
                "architecture": "Wireshark y tcpdump capturan paquetes en tiempo real. Cada protocolo tiene estructura y propósito específico.",
                "security": "El tráfico no cifrado puede ser interceptado. HTTPS protege la confidencialidad de las comunicaciones.",
                "challenge": "Identifica 3 paquetes maliciosos en una captura de 100 paquetes.",
                "fact": "El protocolo TCP/IP fue diseñado para sobrevivir a un ataque nuclear manteniendo la comunicación.",
                "game_type": "packet_analyzer",
                "levels": 8,
                "tools": ["Capturador de paquetes", "Filtro por protocolo", "Inspector de payloads", "Graficador de tráfico"],
                "quiz": [
                    {"q": "¿Qué protocolo usa el puerto 80?", "a": ["FTP", "SSH", "HTTP", "DNS"], "c": 2},
                    {"q": "¿Qué es un payload?", "a": ["La carga útil de datos en un paquete", "Un virus peligroso", "Un tipo de firewall", "Un cable de red"], "c": 0}
                ]
            }
        },
        "script_automation": {
            "icon": "AUTO_FIX",
            "omega": {
                "title": "Automatización con Scripts",
                "intro": "Escribe scripts en Python/Bash para automatizar tareas: procesamiento de archivos, scraping web, análisis de datos.",
                "architecture": "Los scripts son programas que ejecutan tareas secuenciales. Pueden ser activados manualmente o por eventos programados.",
                "security": "Valida todas las entradas en tus scripts. Un script mal escrito puede eliminar datos importantes accidentalmente.",
                "challenge": "Crea un script que procese 100 archivos automáticamente.",
                "fact": "Python es el lenguaje más popular para automatización debido a su sintaxis simple y gran cantidad de librerías.",
                "game_type": "script_lab",
                "levels": 7,
                "tools": ["Editor de código", "Ejecutor de scripts", "Debugger", "Biblioteca de snippets", "Verificador de sintaxis"],
                "quiz": [
                    {"q": "¿Qué es un script?", "a": ["Un documento de texto", "Programa que automatiza tareas", "Un tipo de virus", "Una imagen"], "c": 1},
                    {"q": "¿Qué lenguaje es mejor para automatización?", "a": ["HTML", "Python", "CSS", "SQL"], "c": 1}
                ]
            }
        },
        "forensic_analysis": {
            "icon": "INVESTIGATION",
            "omega": {
                "title": "Análisis Forense Digital",
                "intro": "Recupera evidencia digital de discos, memoria y redes. Análisis post-incidente y preservación de pruebas.",
                "architecture": "El forense sigue cadenas de custodia estrictas. Herramientas como Autopsy y Volatility analizan artifacts.",
                "security": "La evidencia digital es frágil. Un solo bit cambiado puede invalidar toda la evidencia. Documenta todo.",
                "challenge": "Recupera archivos borrados de una imagen de disco y reconstruye la línea temporal de actividades.",
                "fact": "Los forenses pueden recuperar datos incluso después de formatear un disco, usando técnicas de recuperación magnética.",
                "game_type": "forensic_lab",
                "levels": 6,
                "tools": ["Analizador de discos", "Recuperador de archivos", "Analizador de memoria", "Reconstrucción de timeline"],
                "quiz": [
                    {"q": "¿Qué hace un forense digital?", "a": ["Crea virus", "Recupera evidencia digital", "Diseña páginas web", "Envía spam"], "c": 1},
                    {"q": "¿Pueden recuperar datos tras formatear?", "a": ["No", "Sí, con técnicas especiales", "Solo texto", "Solo imágenes"], "c": 1}
                ]
            }
        },
        "api_development": {
            "icon": "API",
            "omega": {
                "title": "Desarrollo de APIs RESTful",
                "intro": "Diseña y construye APIs: autenticación JWT, rate limiting, documentación OpenAPI, versionado.",
                "architecture": "REST usa métodos HTTP estándar. JSON es el formato de intercambio. Las APIs conectan frontend con backend.",
                "security": "Nunca expongas claves API en frontend. Usa HTTPS siempre. Implementa rate limiting para prevenir abuso.",
                "challenge": "Construye una API RESTful completa con autenticación, CRUD y documentación automática.",
                "fact": "El término REST fue definido por Roy Fielding en su tesis doctoral en 2000.",
                "game_type": "api_builder",
                "levels": 5,
                "tools": ["Constructor de endpoints", "Generador de documentación", "Probador de requests", "Analizador de performance"],
                "quiz": [
                    {"q": "¿Qué formato usa REST típicamente?", "a": ["XML", "JSON", "CSV", "TXT"], "c": 1},
                    {"q": "¿Quién definió REST?", "a": ["Bill Gates", "Roy Fielding", "Tim Berners-Lee", "Mark Zuckerberg"], "c": 1}
                ]
            }
        },
        "linux_mastery": {
            "icon": "TERMINAL",
            "omega": {
                "title": "Dominio de Linux",
                "intro": "Domina la línea de comandos Linux: scripting avanzado, administración de sistemas, troubleshooting.",
                "architecture": "El shell interpreta comandos. Pipes conectan salidas con entradas. Scripts automatizan tareas complejas.",
                "security": "Principio de mínimo privilegio. No ejecutes scripts de fuentes no confiables. Verifica checksums.",
                "challenge": "Escribe un script que automatice el despliegue completo de una aplicación web.",
                "fact": "Linux domina el 100% de los supercomputadores del mundo y el 96% de los servidores web.",
                "game_type": "linux_advanced",
                "levels": 8,
                "tools": ["Shell interactivo", "Editor de scripts", "Debugger bash", "Monitor de sistemas"],
                "quiz": [
                    {"q": "¿Qué conectan los pipes?", "a": ["Cables", "Salidas con entradas", "Computadoras", "Redes"], "c": 1},
                    {"q": "¿Qué porcentaje de supercomputadores usan Linux?", "a": ["50%", "75%", "96%", "100%"], "c": 3}
                ]
            }
        },
        "network_security": {
            "icon": "SHIELD",
            "omega": {
                "title": "Seguridad de Redes",
                "intro": "Configura firewalls, IDS/IPS, VPNs. Análisis de tráfico, detección de intrusiones, hardening.",
                "architecture": "Firewalls filtran tráfico por reglas. IDS detecta intrusiones. IPS bloquea activamente amenazas.",
                "security": "Defense in depth: múltiples capas de seguridad. Nunca confíes en una sola protección.",
                "challenge": "Configura una red segura con firewall, IDS y segmentación de red.",
                "fact": "El primer firewall comercial fue desarrollado por Digital Equipment Corporation (DEC) en 1988.",
                "game_type": "network_security_lab",
                "levels": 7,
                "tools": ["Configurador de firewalls", "Analizador de IDS", "Generador de VPNs", "Auditor de seguridad"],
                "quiz": [
                    {"q": "¿Qué hace un firewall?", "a": ["Crea virus", "Filtra tráfico", "Envía correos", "Diseña páginas"], "c": 1},
                    {"q": "¿Qué significa IDS?", "a": ["Internet System", "Intrusion Detection System", "Internal Data Service", "Input Device System"], "c": 1}
                ]
            }
        },
        "kubernetes_master": {
            "icon": "SETTINGS",
            "omega": {
                "title": "Maestría en Kubernetes",
                "intro": "Orquesta contenedores a escala: pods, deployments, services, ingress, auto-scaling.",
                "architecture": "Kubernetes abstrae infraestructura. Declara estado deseado y el sistema lo mantiene automáticamente.",
                "security": "Usa RBAC para control de acceso. Network policies segmentan tráfico. Secrets para credenciales.",
                "challenge": "Despliega una aplicación microservicios con auto-scaling y balanceo de carga.",
                "fact": "Kubernetes fue donado a la Cloud Native Computing Foundation en 2014. Es el estándar de orquestación.",
                "game_type": "k8s_simulator",
                "levels": 9,
                "tools": ["Constructor de clusters", "Gestor de deployments", "Monitor de pods", "Balanceador de servicios"],
                "quiz": [
                    {"q": "¿Qué orquesta Kubernetes?", "a": ["Máquinas virtuales", "Contenedores", "Bases de datos", "Redes"], "c": 1},
                    {"q": "¿Qué es un pod?", "a": ["Una red", "Grupo de contenedores", "Un disco", "Un usuario"], "c": 1}
                ]
            }
        },
        "terraform_infrastructure": {
            "icon": "CLOUD_CIRCLE",
            "omega": {
                "title": "Infraestructura como Código",
                "intro": "Terraform: define infraestructura declarativa. AWS, Azure, GCP. Módulos, estado, planificación.",
                "architecture": "IaC trata infraestructura como software. Versionado, reutilizable, reproducible. Terraform planifica cambios.",
                "security": "No cometas secrets en código. Usa vaults. Revisa planes antes de aplicar. Principio de mínimo privilegio.",
                "challenge": "Construye infraestructura multi-nube con VPC, servidores y bases de datos usando módulos.",
                "fact": "Terraform fue creado por HashiCorp en 2014. Es la herramienta IaC más popular de la industria.",
                "game_type": "iac_builder",
                "levels": 7,
                "tools": ["Editor HCL", "Planificador de cambios", "Gestor de estado", "Constructor de módulos"],
                "quiz": [
                    {"q": "¿Qué es IaC?", "a": ["Infraestructura como Código", "Internet como Cloud", "Input como Code", "Internal Application Control"], "c": 0},
                    {"q": "¿Quién creó Terraform?", "a": ["Google", "HashiCorp", "Microsoft", "Amazon"], "c": 1}
                ]
            }
        },
        "advanced_cryptography": {
            "icon": "ENCRYPTION",
            "omega": {
                "title": "Criptografía Post-Cuántica",
                "intro": "Prepara sistemas para computación cuántica: algoritmos resistentes, criptografía de curvas elípticas.",
                "architecture": "Shor's algorithm rompe RSA/ECC cuánticamente. NTRU, lattice-based, hash-based son resistentes.",
                "security": "La criptografía actual será obsoleta con computadoras cuánticas. Migra temprano a estándares post-cuánticos.",
                "challenge": "Implementa un sistema de cifrado híbrido clásico-cuántico resistente.",
                "fact": "NIST está estandarizando algoritmos post-cuánticos desde 2016. Se espera computadoras cuánticas para 2030.",
                "game_type": "post_quantum_crypto",
                "levels": 8,
                "tools": ["Generador de claves post-cuánticas", "Simulador cuántico", "Analizador de resistencia", "Migrador de sistemas"],
                "quiz": [
                    {"q": "¿Qué rompe Shor's algorithm?", "a": ["Hash SHA-256", "RSA/ECC", "AES-256", "MD5"], "c": 1},
                    {"q": "¿Cuándo se esperan computadoras cuánticas?", "a": ["2025", "2030", "2050", "Nunca"], "c": 1}
                ]
            }
        }
    }

    @classmethod
    def get_unit(cls, unit_id: str, protocol: str):
        unit = cls.UNITS.get(unit_id)
        if not unit:
            return None
        
        content = unit.get(protocol)
        if not content:
            return None
            
        return {
            "id": unit_id,
            "icon": unit["icon"],
            **content
        }

    @classmethod
    def get_all_units(cls, protocol: str):
        units = []
        for unit_id in cls.UNITS:
            unit = cls.get_unit(unit_id, protocol)
            if unit is not None:
                units.append(unit)
        return units
