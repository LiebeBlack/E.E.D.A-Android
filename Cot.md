# I.S.D.I — CONTEXTO DE PROYECTO (PARA AGENTES IA)

## 🎯 PROPÓSITO DEL PROYECTO

**I.S.D.I (Isla Digital / Instituto de Seguridad Digital e Interactiva)** es una plataforma educativa modular diseñada para enseñar alfabetización digital: hardware, software, redes, ciberseguridad, ética y herramientas de IA a usuarios de entre **3 y 16 años**.

La plataforma se basa en el modelo pedagógico **CPA (Concreto–Pictórico–Abstracto)** y en una narrativa de gamificación interactiva. Su principio rector es: **"código limpio, completo, bien documentado y funcional"**, con exploración progresiva de cada área temática y su estructura interna.

---

## 🛠️ STACK TECNOLÓGICO

| Capa | Tecnología |
|---|---|
| **Core** | Python 3.12 |
| **UI Framework** | [Flet](https://flet.dev) v0.27.3 (Flutter/Python) |
| **Persistencia** | SQLite3 — `src/isla_digital.db` |
| **Arquitectura** | Modular, basada en componentes y eventos centralizados |

---

## 🏗️ ESTRUCTURA DE ARCHIVOS

```
src/
├── main.py              # Punto de entrada: rutas y secuencia de arranque
├── core/
│   ├── content.py       # Motor pedagógico: textos, desafíos y unidades temáticas
│   ├── theme.py         # Sistema de diseño: DesignTokens, colores por protocolo, Glassmorphism
│   ├── database.py      # Gestión de progreso y respuestas de usuarios (SQLite3)
│   └── event_bus.py     # Comunicación asíncrona desacoplada entre módulos
├── modules/
│   ├── dashboard.py     # Resumen de estado y bienvenida personalizada
│   ├── zones.py         # Mapa de unidades educativas (lectura e interacción)
│   ├── lab.py           # Taller interactivo de desafíos prácticos
│   └── security.py      # Centro de mejores prácticas y métricas de seguridad
└── components/          # Elementos UI reutilizables: Sidebar, GlassContainer, etc.
```

---

## 🌌 SISTEMA DE PROTOCOLOS ADAPTATIVOS

La aplicación se adapta visual y semánticamente según el **rango de edad seleccionado**. Cada protocolo define una narrativa, paleta de color y nivel de lenguaje diferente:

| Protocolo | Edad | Narrativa | Color Principal | Lenguaje |
|---|---|---|---|---|
| **ALPHA** | 3–7 años | Exploradores | `#00C853` (Verde) | Lúdico, simple e intuitivo |
| **DELTA** | 8–12 años | Operadores | `#00B0FF` (Azul) | Técnico introductorio |
| **OMEGA** | 13–16 años | Arquitectos | `#FF3D00` (Rojo/Naranja) | Técnico profesional / hacker |

> **Regla crítica:** Ningún texto, color ni componente UI puede definirse de forma fija (*hardcoded*). Todo debe fluir desde `DesignTokens` y la lógica condicional del protocolo activo.

---

## 📖 UNIDADES PEDAGÓGICAS

El contenido en `src/core/content.py` se divide en **8 áreas temáticas**, cada una con niveles progresivos que van desde conceptos básicos hasta avanzados:

| ID | Área | Rango temático |
|---|---|---|
| `hardware` | Hardware | Componentes físicos → Arquitectura de computadoras |
| `logic` | Lógica | Pensamiento computacional → Algoritmos y estructuras de datos |
| `network` | Redes | Conectividad básica → Topología de redes |
| `cybersecurity` | Ciberseguridad | Protección de datos → Criptografía y ciberdefensa |
| `os` | Sistemas Operativos | Fundamentos → Kernels y virtualización |
| `ai` | Inteligencia Artificial | Conceptos básicos → Ética del algoritmo |
| `programming` | Programación | Introducción al código → Paradigmas y POO |
| `ethics` | Ética Digital | Ciudadanía digital → Sesgo algorítmico |

---

## 🤖 GUÍA PARA AGENTES IA

Al trabajar en este código, sigue **obligatoriamente** estas políticas:

1. **Respeta los DesignTokens**
   - Todo valor visual (color, tipografía, espaciado) debe obtenerse desde `src/core/theme.py` → clase `DesignTokens`.
   - **Prohibido:** valores de color o tamaño definidos directamente en el código (*hardcoded*).

2. **Adapta siempre al Protocolo activo**
   - Antes de cualquier cambio en UI o contenido, verifica si afecta a Alpha, Delta u Omega.
   - Usa la lógica condicional correspondiente para cada protocolo.

3. **Modularidad estricta**
   - Nuevas funcionalidades de lógica → buscar primero en `src/modules/`.
   - Nuevos elementos visuales reutilizables → crear en `src/components/`.
   - Nunca mezclar lógica de negocio con lógica de presentación.

4. **Persistencia centralizada**
   - Todo progreso, respuesta o estado de usuario debe guardarse **exclusivamente** a través de `src/core/database.py`.
   - No acceder directamente a la base de datos desde módulos o componentes.

5. **Comunicación entre módulos**
   - Usar `src/core/event_bus.py` para toda comunicación entre módulos.
   - Evitar referencias directas cruzadas entre módulos.

6. **Calidad del código**
   - Código limpio, completo y documentado en cada entrega.
   - Nombres de variables y funciones en inglés (snake_case).
   - Comentarios y docstrings en español cuando el contexto pedagógico lo requiera.

---

*Este documento fue generado para optimizar el contexto y el ahorro de tokens en interacciones con agentes IA. Versión alineada con README.md y políticas del proyecto.*
