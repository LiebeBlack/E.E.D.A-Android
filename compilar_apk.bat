@echo off
setlocal
echo =======================================
echo 🏝️ ISLA DIGITAL - Compilador de APK 🏝️
echo =======================================
echo.
echo Iniciando proceso de compilación... (Android Studio 2026 Ready)
echo.

call gradlew.bat assembleDebug --no-daemon

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ ¡COMPILACIÓN EXITOSA!
    echo.
    echo 📁 El APK se encuentra en:
    echo %cd%\app\build\outputs\apk\debug\app-debug.apk
    echo.
    echo Puedes instalarlo en tu dispositivo o emulador.
) else (
    echo.
    echo ❌ ERROR EN LA COMPILACIÓN.
    echo Por favor, revisa los mensajes de arriba para solucionar los problemas.
)

echo.
pause
