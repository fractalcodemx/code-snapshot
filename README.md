# Code Snapshot by Fractalcode

**Code Snapshot** es una herramienta de línea de comandos desarrollada en Python para capturar un "snapshot" completo y autocontenido de un proyecto de software. Consolida la estructura de archivos, el contenido de cada fichero y metadatos clave del historial de Git en un único archivo de texto (`.txt`).

El propósito principal es generar un contexto exhaustivo y fácil de procesar, ideal para documentación, análisis de código, archivado o para ser utilizado como base de conocimiento en Grandes Modelos de Lenguaje (LLMs).

## Características

*   **Snapshot Unificado**: Genera un solo archivo `.txt` con el contenido de todo el proyecto.
*   **Metadatos de Git**: Incluye información del último commit (hash, autor, fecha) para cada archivo, proporcionando trazabilidad.
*   **Altamente Configurable**: Utiliza un archivo `config.json` para definir fácilmente qué directorios, archivos o extensiones excluir.
*   **Formato Limpio y Estructurado**: La salida está formateada con separadores claros para ser legible tanto por humanos como por máquinas.
*   **Barra de Progreso Interactiva**: Muestra el progreso en tiempo real sin saturar la consola.
*   **Modo de Prueba Rápida**: Incluye un flag `--limit` para procesar solo un número limitado de archivos, ideal para pruebas y depuración.

## Prerrequisitos

*   Python 3.x
*   Git

## Instalación y Configuración

Sigue estos pasos para configurar el entorno y preparar la herramienta para su uso.

1.  **Clona el repositorio:**
    ```bash
    git clone git@gitlab.com:fractalcodemx/code-snapshot.git
    cd code-snapshot
    ```

2.  **Crea y activa un entorno virtual:**
    Esto aísla las dependencias del proyecto.
    ```bash
    # Crear el entorno
    python -m venv .venv

    # Activar en Windows (PowerShell/VSCode Terminal)
    .venv\Scripts\activate

    # Activar en Linux/macOS
    # source .venv/bin/activate
    ```

3.  **Instala las dependencias:**
    El archivo `requirements.txt` contiene todas las librerías necesarias.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura el proyecto a analizar:**
    a. Copia la plantilla de configuración:
    ```bash
    # En Windows
    copy config.template.json config.json

    # En Linux/macOS
    # cp config.template.json config.json
    ```
    b. Abre `config.json` y edita los valores para que apunten a tu proyecto. El campo más importante es `project_root`.

    ```json
    {
        "project_root": "C:/path/to/your/project",
        "output_directory": "output",
        "ignored_patterns": [
            "node_modules",
            "vendor",
            ".git",
            ".vscode",
            ".DS_Store",
            "composer.lock",
            "output"
        ],
        "ignored_file_extensions": [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".svg",
            ".ico",
            ".woff",
            ".woff2",
            ".ttf",
            ".otf",
            ".eot",
            ".zip",
            ".tar",
            ".gz",
            ".rar",
            ".7z",
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".psd",
            ".ai",
            ".sketch",
            ".db",
            ".sqlite",
            ".md",
            ".map"
        ]
    }
    ```

## Uso

Una vez configurado, puedes generar snapshots con los siguientes comandos.

#### Generar un snapshot completo

Ejecuta el script sin argumentos para procesar todos los archivos del proyecto configurado.

```bash
python src/snapshot_generator.py