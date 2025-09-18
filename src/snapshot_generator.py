# src/snapshot_generator.py
import os
import json
import datetime

def generate_code_snapshot(config_path="config.json"):
    # 1. Leer la configuración
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo de configuración '{config_path}' no fue encontrado.")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo de configuración '{config_path}' tiene un formato JSON inválido.")
        return

    project_root = config.get("project_root")
    output_dir = config.get("output_directory")
    ignored_patterns = config.get("ignored_patterns")
    ignored_extensions = config.get("ignored_file_extensions")

    if not project_root:
        print("Error: 'project_root' no está definido en el archivo de configuración.")
        return

    print(f"Configuración cargada exitosamente para el proyecto: {project_root}")
    print(f"Directorio de salida: {output_dir}")
    print(f"Patrones ignorados: {ignored_patterns}")
    print(f"Extensiones ignoradas: {ignored_extensions}")

    # Aquí irá el resto de la lógica en pasos futuros

if __name__ == "__main__":
    # Asegurarse de que el script se ejecuta desde la raíz del repositorio
    # o ajustar la ruta del config.json si está en otro lugar
    generate_code_snapshot(config_path="config.json")