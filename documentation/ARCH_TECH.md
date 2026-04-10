# 🏝️ Isla Digital - Flet Edition
> **Versión:** 0.7.3  
> **Arquitectura:** Clean Architecture & Modular System  
> **Stack:** Python | Flet | SQLite

**Isla Digital (I.S.D.I)** es una plataforma educativa interactiva orientada a la alfabetización digital. Esta versión, desarrollada íntegramente en **Flet**, prioriza la modularidad, la eficiencia en el consumo de memoria y la separación estricta de responsabilidades.

---

## 🏗️ Estructura del Proyecto (Clean Architecture)

El sistema se organiza de forma que el núcleo pedagógico sea independiente de la interfaz, facilitando el mantenimiento y la escalabilidad.

```text
isla_digital_flet/
├── base/                # Interfaces y Clases Abstractas (Contratos)
│   └── module.py        # BaseModule (ABC para estandarizar módulos)
├── core/                # El "Kernel" del sistema (Lógica de Negocio)
│   ├── content.py       # Motor pedagógico (Protocolos Alpha, Delta, Omega)
│   ├── database.py      # Persistencia SQLite y gestión de progreso
│   ├── event_bus.py     # Comunicación desacoplada (Pub/Sub)
│   └── theme.py         # Design Tokens y gestión de UI dinámica
├── components/          # Librería de UI Reutilizable
│   ├── glass_container.py   # Contenedores con efecto Glassmorphism
│   ├── sidebar.py           # Navegación lateral adaptativa
│   └── technical_diagram.py # Render de diagramas interactivos
├── modules/             # Funcionalidades de Usuario (Features)
│   ├── dashboard.py     # Telemetría de usuario y bienvenida
│   ├── zones.py         # Unidades de aprendizaje y retos
│   └── security.py      # Módulo de mejores prácticas digitales
├── main.py              # Orquestador y selector de protocolos
└── isla_digital.db      # DB persistente (Autogenerada)
