# Isla Digital - Script de Compilacion Automatica
# PowerShell Script para Windows

param(
    [string]$Plataforma = "android",
    [switch]$SkipAssets = $false,
    [switch]$SkipTests = $false
)

# Configuracion
$ProjectPath = "C:\Users\Yolanda\Desktop\v0.0.1\isla_digital"
$LogFile = "$ProjectPath\compilacion_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# Funciones de log
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    if (Test-Path $LogFile) {
        Add-Content -Path $LogFile -Value $logMessage
    } else {
        $logMessage | Out-File -FilePath $LogFile -Append
    }
}

function Test-CommandExists {
    param([string]$Command)
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

function Test-FlutterInstalled {
    Write-Log "Verificando instalacion de Flutter..."
    if (-not (Test-CommandExists "flutter")) {
        Write-Log "Flutter no encontrado en el PATH." "WARN"
        return $false
    }
    Write-Log "Flutter detectado correctamente." "SUCCESS"
    return $true
}

function Test-AndroidSDK {
    Write-Log "Verificando Android SDK..."
    if (-not $env:ANDROID_SDK_ROOT -and -not $env:ANDROID_HOME) {
        Write-Log "Variables de Android SDK no detectadas." "WARN"
    } else {
        Write-Log "Android SDK configurado." "SUCCESS"
    }
}

function Install-FlutterDependencies {
    Write-Log "=== INSTALANDO DEPENDENCIAS ==="
    Set-Location $ProjectPath
    & flutter pub get
}

function Build-Android {
    Write-Log "=== COMPILANDO APK ==="
    Set-Location $ProjectPath
    & flutter build apk --release
    return $LASTEXITCODE -eq 0
}

function Build-Windows {
    Write-Log "=== COMPILANDO WINDOWS ==="
    Set-Location $ProjectPath
    & flutter build windows --release
    return $LASTEXITCODE -eq 0
}

function Show-Summary {
    Write-Log "========================================"
    Write-Log "    RESUMEN DE COMPILACION"
    Write-Log "========================================"
    
    $apk = "$ProjectPath\build\app\outputs\flutter-apk\app-release.apk"
    $windows = "$ProjectPath\build\windows\x64\runner\Release\Isla Digital.exe"
    
    if (Test-Path $apk) {
        $size = [math]::Round((Get-Item $apk).Length / 1MB, 2)
        Write-Log "OK - Android APK generado ($($size) MB)" "SUCCESS"
    }
    
    if (Test-Path $windows) {
        $size = [math]::Round((Get-Item $windows).Length / 1MB, 2)
        Write-Log "OK - Windows EXE generado ($($size) MB)" "SUCCESS"
    }
}

# --- SCRIPT PRINCIPAL ---
Write-Log "INICIANDO PROCESO ISLA DIGITAL"
if (-not (Test-FlutterInstalled)) { exit 1 }
Test-AndroidSDK
Install-FlutterDependencies

$success = $false
switch ($Plataforma.ToLower()) {
    "android" { $success = Build-Android }
    "windows" { $success = Build-Windows }
    "all"     { 
        $res1 = Build-Android
        $res2 = Build-Windows
        $success = $res1 -or $res2
    }
}

Show-Summary
Write-Log "Proceso terminado."