# 🏝️ ISLA DIGITAL (I.S.D.I) // REPOSITORIO MAESTRO

> **SYSTEM_VERSION:** `4.2.0-TOTAL`  
> **CORE_ARCHITECTURE:** `Clean Architecture / Modular Core`  
> **UI_ENGINE:** `Flet | Python | SQLite`

---

## 🏗️ CATASTRO DE ARQUITECTURA
El sistema está diseñado bajo una arquitectura de **Separación de Responsabilidades (SoC)**, asegurando que el motor lógico y pedagógico sea independiente de la interfaz visual.



| Directorio | Responsabilidad Técnica |
| :--- | :--- |
| **`main.py`** | Orquestador universal de arranque y enrutamiento dinámico. |
| **`base/`** | Capa de Abstracción: Define los contratos funcionales (Clases Abstractas). |
| **`core/`** | Kernel Lógico: Gestión de eventos, persistencia, temas y motor de datos. |
| **`components/`** | Biblioteca de UI Atómica: Glassmorphism, Sidebars, Diagramas. |
| **`modules/`** | Capa de Aplicación: Implementación de features (Dashboard, Zonas, Security). |

---

## 💻 ESPECIFICACIONES DE KERNEL

### 1. Sistema de Comunicación
El proyecto implementa un **Event Bus (Pub/Sub)** interno para el desacoplamiento de módulos, permitiendo una comunicación asíncrona robusta sin dependencias circulares.

### 2. Capa de Persistencia
La base de datos `isla_digital.db` (SQLite) gestiona automáticamente el estado y progreso del usuario, permitiendo la reanudación de sesiones pedagógicas.



### 3. Motor Pedagógico
Basado en tres niveles de protocolo (**Alpha, Delta, Omega**), el motor ajusta los componentes de interfaz en tiempo real según el nivel seleccionado mediante **Design Tokens** centralizados.

---

## 🚀 GUÍA DE IMPLEMENTACIÓN Y DESPLIEGUE
Este sistema está optimizado para entornos de bajo consumo (Debian/LXDE).

1. **Clonación del repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/isla_digital_flet.git](https://github.com/tu-usuario/isla_digital_flet.git)
   cd isla_digital_flet
