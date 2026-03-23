@echo off
setlocal enabledelayedexpansion
title 🏝️ ISLA DIGITAL - Suite de Compilacion Profesional 🚀

:: ========================================================
:: CONFIGURACION Y REQUISITOS
:: ========================================================
:INIT
set "LOG_FILE=compilacion_reporte.log"
set "APK_DEBUG=app\build\outputs\apk\debug\app-debug.apk"
set "APK_RELEASE=app\build\outputs\apk\release\app-release-unsigned.apk"

:MENU
cls
echo ========================================================
echo   🏝️  ISLA DIGITAL - SISTEMA AVANZADO DE APK v2.0
echo ========================================================
echo.
echo [1] 🛠️  LIMPIEZA PROFUNDA (Caches, Gradlew Clean, Build)
echo [2] 🚀  MODO DEBUG   (Rapido, para pruebas)
echo [3] 👑  MODO RELEASE (Final, optimizado)
echo [4] 📱  INSTALAR ULTIMO APK (Requiere ADB conectado)
echo [5] 📁  ABRIR CARPETA DE SALIDA
echo [6] ❌  SALIR
echo.
echo ========================================================
if exist %LOG_FILE% (
    echo [TIP] Se ha generado un log previo: %LOG_FILE%
)
echo.

set /p choice="Seleccione una operacion (1-6): "

if "%choice%"=="1" goto CLEAN
if "%choice%"=="2" set BUILD_TYPE=assembleDebug && set APK_TARGET=%APK_DEBUG% && goto PROCESS
if "%choice%"=="3" set BUILD_TYPE=assembleRelease && set APK_TARGET=%APK_RELEASE% && goto PROCESS
if "%choice%"=="4" goto INSTALL_ADB
if "%choice%"=="5" start "" "app\build\outputs\apk\" && goto MENU
if "%choice%"=="6" exit
goto MENU

:CLEAN
echo.
echo 🧹 Iniciando saneamiento total...
echo [1/3] Eliminando carpetas de cache locales...
if exist ".gradle" rd /s /q .gradle
if exist "app\build" rd /s /q app\build
if exist "build" rd /s /q build

echo [2/3] Ejecutando comando de limpieza Gradle...
call gradlew.bat clean --no-daemon > %LOG_FILE% 2>&1
if !ERRORLEVEL! equ 0 (
    echo [3/3] ✨ ¡Proyecto purificado! Todo se regenerara en la proxima compilacion.
) else (
    echo ⚠️ Error en gradlew clean. Revisa %LOG_FILE%
)
pause
goto MENU

:PROCESS
echo.
echo 🔎 Verificando Entorno...
java -version >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo ❌ ERROR: Java no esta instalado o no esta en el PATH.
    pause
    goto MENU
)

echo 🚀 Compilando: !BUILD_TYPE!...
echo (Esto puede tardar unos minutos dependiendo de los cambios...)
echo.

:: Ejecutamos la compilacion mandando errores detallados al log Y a la pantalla
call gradlew.bat clean !BUILD_TYPE! --no-daemon --stacktrace --info --warning-mode all 2>&1 | tee %LOG_FILE%
:: Nota: Si 'tee' no existe en Windows (por defecto no), usamos redireccion simple
if !ERRORLEVEL! neq 0 (
    call gradlew.bat clean !BUILD_TYPE! --no-daemon --stacktrace --info --warning-mode all > %LOG_FILE% 2>&1
)

if !ERRORLEVEL! equ 0 (
    echo.
    echo ========================================================
    echo   ✅ ¡COMPILACION TERMINADA CON EXITO!
    echo ========================================================
    echo 📦 APK: !APK_TARGET!
    echo.
    echo ¿Deseas abrir la carpeta del APK ahora? (S/N)
    set /p op_open="> "
    if /i "!op_open!"=="S" start "" "app\build\outputs\apk\"
    goto MENU
) else (
    goto ERROR_DETALLADO
)

:INSTALL_ADB
echo.
echo 📱 Buscando dispositivos...
adb devices
echo Intentando instalar !APK_TARGET!...
adb install -r !APK_TARGET!
if !ERRORLEVEL! equ 0 (
    echo ✅ Instalado correctamente.
) else (
    echo ❌ Fallo la instalacion. Verifica el cable USB o la depuracion ADB.
)
pause
goto MENU

:ERROR_DETALLADO
echo.
echo ========================================================
echo   ❌ ERROR CRITICO DETECTADO
echo ========================================================
echo.
echo Detalles tecnicos capturados en: %LOG_FILE%
echo.
echo Mostrando las ultimas lineas del error:
echo --------------------------------------------------------
powershell -command "Get-Content %LOG_FILE% -Tail 15"
echo --------------------------------------------------------
echo.
echo Intenta la Opcion [1] si los errores persisten.
pause
goto MENU
