import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_header(text: str):
    print("\n" + "=" * 60)
    print(f" {text.center(58)} ")
    print("=" * 60)

def main():
    print_header("I.S.D.I-PC - SCRIPT DE EMPAQUETADO UNIVERSAL (NATIVO DIR)")
    
    root_dir = Path(__file__).parent.resolve()
    release_dir = root_dir / "Release_ISDI_PC"
    src_dir = root_dir / "src"
    
    print("\n[+] Preparando carpeta de compilación: 'Release_ISDI_PC'...")
    if release_dir.exists():
        try:
            shutil.rmtree(release_dir)
        except Exception as e:
            pass
            
    release_dir.mkdir(parents=True, exist_ok=True)
    
    print("[+] Copiando código fuente al entorno seguro...")
    release_src = release_dir / "src"
    shutil.copytree(src_dir, release_src)
    shutil.copy2(root_dir / "requirements.txt", release_dir / "requirements.txt")
    if (root_dir / "README.md").exists():
        shutil.copy2(root_dir / "README.md", release_dir / "README.md")

    # 3. Script Batch Windows (PyInstaller Onedir)
    windows_script = release_dir / "build_windows.bat"
    windows_script.write_text(
        "@echo off\n"
        "title Compilador I.S.D.I - Windows\n"
        "echo =======================================================\n"
        "echo    CONSTRUYENDO APLICACION INSTALABLE (CARPETA) WINDOWS\n"
        "echo =======================================================\n"
        "echo [1/2] Verificando e Instalando dependencias...\n"
        "pip install -r requirements.txt pyinstaller\n"
        "echo.\n"
        "echo [2/2] Empaquetando la aplicacion (Modo Carpeta y Path Src)...\n"
        "REM Usamos pyinstaller directamente para forzar el modo carpeta y arreglar el PATH de importaciones\n"
        "pyinstaller --noconfirm --windowed --onedir --name \"ISDI-PC\" --paths src --add-data \"src;src\" src/main.py\n"
        "echo.\n"
        "echo =======================================================\n"
        "echo [ OK ] ¡Compilacion Finalizada!\n"
        "echo El programa se encuentra DENTRO de la carpeta:\n"
        "echo 'dist/ISDI-PC/' y el archivo ejecutable esta ahi dentro.\n"
        "echo =======================================================\n"
        "pause\n"
    )

    # 4. Script Linux Nativo
    linux_script = release_dir / "build_linux.sh"
    linux_script.write_text(
        "#!/bin/bash\n"
        "echo \"=======================================================\"\n"
        "echo \"   CONSTRUYENDO APLICACION INSTALABLE PARA LINUX\"\n"
        "echo \"=======================================================\"\n"
        "echo \"[1/2] Verificando dependencias...\"\n"
        "python3 -m pip install -r requirements.txt pyinstaller\n"
        "echo \"\"\n"
        "echo \"[2/2] Empaquetando la aplicacion...\"\n"
        "pyinstaller --noconfirm --windowed --onedir --name \"ISDI-PC\" --paths src --add-data \"src:src\" src/main.py\n"
        "echo \"\"\n"
        "echo \"=======================================================\"\n"
        "echo \"[ OK ] ¡Compilacion Finalizada!\"\n"
        "echo \"La carpeta del ejecutable esta en 'dist/ISDI-PC/'\"\n"
        "echo \"=======================================================\"\n"
    )

    # 5. Dockerfile
    dockerfile = release_dir / "Dockerfile"
    dockerfile.write_text(
        "FROM python:3.11-slim\n\n"
        "RUN apt-get update && apt-get install -y \\\n"
        "    build-essential \\\n"
        "    libgtk-3-dev \\\n"
        "    pkg-config \\\n"
        "    && rm -rf /var/lib/apt/lists/*\n\n"
        "WORKDIR /app\n"
        "COPY requirements.txt .\n"
        "RUN pip install -r requirements.txt pyinstaller\n\n"
        "COPY src/ ./src/\n\n"
        "CMD pyinstaller --noconfirm --windowed --onedir --name \"ISDI-PC\" --paths src --add-data \"src:src\" src/main.py && cp -r dist /app/out/\n"
    )

    docker_script = release_dir / "build_linux_via_docker.bat"
    docker_script.write_text(
        "@echo off\n"
        "title Compilador I.S.D.I - Linux via Docker\n"
        "echo =======================================================\n"
        "echo    COMPILANDO PARA LINUX (COMPATIBILIDAD VIRTUAL)\n"
        "echo =======================================================\n"
        "echo ADVERTENCIA: Docker Desktop debe de estar ejecutandose.\n"
        "echo.\n"
        "mkdir out 2>nul\n"
        "echo [1/2] Construyendo el entorno base seguro...\n"
        "docker build -t isdi-linux-builder .\n"
        "IF %ERRORLEVEL% NEQ 0 (\n"
        "    echo [!] Error: No se pudo conectar a Docker o compilar.\n"
        "    pause\n"
        "    exit /b %ERRORLEVEL%\n"
        ")\n"
        "echo [2/2] Empaquetando internamente y extrayendo las carpetas...\n"
        "docker run --rm -v \"%CD%\\out:/app/out\" isdi-linux-builder\n"
        "echo.\n"
        "echo =======================================================\n"
        "echo [ OK ] ¡Compilacion Completada Exitosamente!\n"
        "echo Revisa la subcarpeta: Release_ISDI_PC\\out\\dist\\ISDI-PC\\\n"
        "echo =======================================================\n"
        "pause\n"
    )

    print_header("🎯 ESTADO: ENTORNO LISTO PARA COMPILAR")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        os.chdir(release_dir)
        subprocess.call(["build_windows.bat"], shell=True)
    else:
        print("¿Deseas iniciar la compilación para Windows ahora mismo?")
        choice = input("Ingresa '1' para compilar ahora (o presiona Enter para salir): ")
        if choice.strip() == "1":
            os.chdir(release_dir)
            subprocess.call(["build_windows.bat"], shell=True)
        else:
            print(f"\n[✓] ¡Todo listo! Reinicie su compilación ejecutando build.bat en la raíz.")

if __name__ == "__main__":
    main()
