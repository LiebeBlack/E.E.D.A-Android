# Guía de Contribución para E.E.D.A.

¡Antes que nada, gracias por considerar contribuir a **E.E.D.A. (Ecosistema Educativo Digital Adaptable)**! Es gracias a personas como tú que este ecosistema pedagógico sigue evolucionando para transformar la educación.

---

## ¿Por dónde empezar?

- **Reporte de Errores (Bug Reports)**: Si notas un fallo técnico o una inconsistencia visual, por favor abre un *issue* utilizando nuestra plantilla de reporte de errores.
- **Solicitud de Funciones (Feature Requests)**: ¿Tienes una idea para potenciar el sistema o añadir un nuevo módulo pedagógico? Utiliza la plantilla de solicitud de funciones o contáctanos a través de la sección de contacto en nuestra página web oficial para hacérnoslo saber.
- **Documentación**: Las mejoras en la redacción, correcciones ortográficas o nuevos ejemplos de implementación son siempre bienvenidas y fundamentales.

---

## Cómo contribuir

Para mantener un flujo de desarrollo limpio y profesional, seguimos el modelo estándar de GitHub:

1.  **Realiza un Fork** del repositorio oficial.
2.  Crea tu **rama de función** (`git checkout -b feature/nueva-funcion-increible`).
3.  **Confirma (Commit)** tus cambios con mensajes claros y descriptivos (`git commit -m 'Añadir módulo de lógica adaptativa'`).
4.  **Sube (Push)** los cambios a tu rama en GitHub (`git push origin feature/nueva-funcion-increible`).
5.  ¡Abre un **Pull Request** para que revisemos tu propuesta!

---

## 💻 Configuración de Desarrollo

Sigue estos comandos para ejecutar y probar el proyecto en tu entorno local:

```powershell
# 1. Clonar el repositorio oficial
git clone [https://github.com/LiebeBlack/E.E.D.A.git](https://github.com/LiebeBlack/E.E.D.A.git)

# 2. Entrar al directorio del proyecto
cd E.E.D.A

# 3. Instalar las dependencias necesarias
pip install -r requirements.txt

# 4. Ejecutar el ecosistema localmente
python src/main.py
