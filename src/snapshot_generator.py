# src/snapshot_generator.py
import os
import sys
import json
import datetime
import re
import argparse
from git import Repo, InvalidGitRepositoryError
from colorama import init, Fore, Style

init(autoreset=True)

class Colors:
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    RESET = Style.RESET_ALL

def print_progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """
    Dibuja una barra de progreso en la terminal.
    """
    if total == 0:
        total = 1
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')

def get_git_commit_info(filepath, repo_path):
    # ... (Esta función no necesita cambios)
    try:
        repo = Repo(repo_path)
        relative_filepath = os.path.relpath(filepath, repo_path)
        commits = list(repo.iter_commits(paths=relative_filepath, max_count=1))
        if commits:
            commit = commits[0]
            author = commit.author.name
            date = datetime.datetime.fromtimestamp(commit.authored_date, tz=datetime.timezone.utc).astimezone(datetime.datetime.now().astimezone().tzinfo).strftime('%Y-%m-%d %H:%M:%S')
            hexsha = commit.hexsha[:7]
            return f"{hexsha} ({author}) on {date}"
        return "N/A (No commit info)"
    except InvalidGitRepositoryError:
        return "N/A (Not a Git repository at project root)"
    except Exception:
        return "N/A (File not tracked by Git)"

def generate_code_snapshot(config_path="config.json", limit=-1):
    # 1. Leer la configuración
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"{Colors.RED}Error: Configuration file '{config_path}' not found.")
        return
    except json.JSONDecodeError:
        print(f"{Colors.RED}Error: Configuration file '{config_path}' has an invalid JSON format.")
        return

    project_root = config.get("project_root")
    output_dir = config.get("output_directory", "output")
    ignored_patterns = config.get("ignored_patterns", [])
    ignored_extensions = config.get("ignored_file_extensions", [])

    if not project_root:
        print(f"{Colors.RED}Error: 'project_root' is not defined in the configuration file.")
        return

    project_root = os.path.abspath(project_root)

    print(f"{Colors.BLUE}=======================================================================")
    print(f"{Colors.CYAN}  INITIALIZING SNAPSHOT FOR PROJECT: {os.path.basename(project_root)}")
    print(f"{Colors.BLUE}=======================================================================")

    # --- FASE 1: DESCUBRIMIENTO Y FILTRADO DE ARCHIVOS ---
    print(f"{Colors.CYAN}Phase 1: Discovering and filtering files...")
    files_to_process = []
    for root, dirs, files in os.walk(project_root, topdown=True):
        dirs[:] = [d for d in dirs if not any(pattern in os.path.join(os.path.relpath(root, project_root), d).replace(os.sep, '/') for pattern in ignored_patterns)]
        for file in files:
            relative_file_path = os.path.join(os.path.relpath(root, project_root), file)
            if any(pattern in relative_file_path.replace(os.sep, '/') for pattern in ignored_patterns):
                continue
            if any(file.endswith(ext) for ext in ignored_extensions):
                continue
            files_to_process.append(os.path.join(root, file))

    total_files_found = len(files_to_process)
    if total_files_found == 0:
        print(f"{Colors.YELLOW}No files found to process with the current filters.")
        return

    if limit > 0:
        print(f"{Colors.YELLOW}Found {total_files_found} files. Processing the first {limit} due to --limit flag.\n")
        files_to_process = files_to_process[:limit]
    else:
        print(f"{Colors.GREEN}Found {total_files_found} files to process.\n")

    total_files_to_process = len(files_to_process)

    # --- FASE 2: PROCESAMIENTO Y ESCRITURA DEL SNAPSHOT ---
    print(f"{Colors.CYAN}Phase 2: Generating snapshot...")

    project_name_slug = re.sub(r'[^a-zA-Z0-9_-]', '', os.path.basename(project_root)).lower()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(output_dir, f"{project_name_slug}_snapshot_{timestamp}.txt")

    # --- CONFIGURACIÓN DE FORMATO DE SALIDA ---
    # Define el ancho total para las líneas separadoras. ¡Cambia este valor para ajustar todo el formato!
    LINE_WIDTH = 150
    HEADER_LINE = "=" * LINE_WIDTH
    SEPARATOR_LINE = "-" * LINE_WIDTH

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(f"{HEADER_LINE}\n")
        outfile.write("Fractalcode - Code Snapshot\n")
        outfile.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (America/Mexico_City)\n")
        outfile.write(f"Project: {os.path.basename(project_root)}\n")
        outfile.write(f"Root Directory: {project_root}\n")
        outfile.write(f"{HEADER_LINE}\n\n")

        print_progress_bar(0, total_files_to_process, prefix='Progress:', suffix='Completed', length=50)

        for i, file_path in enumerate(files_to_process):
            relative_path = os.path.relpath(file_path, project_root).replace(os.sep, '/')
            commit_info = get_git_commit_info(file_path, project_root)

            # --- CALCULO DINÁMICO DE SEPARADORES ---
            start_tag = "--- FILE START "
            content_tag = "--- FILE CONTENT "
            end_tag = "--- FILE END "

            outfile.write(f"{SEPARATOR_LINE}\n")
            outfile.write(f"{start_tag}{'-' * (LINE_WIDTH - len(start_tag))}\n")
            outfile.write(f"Full Path: {relative_path}\n")
            outfile.write(f"Last Commit: {commit_info}\n")
            outfile.write(f"{content_tag}{'-' * (LINE_WIDTH - len(content_tag))}\n")
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            except Exception as e:
                outfile.write(f"ERROR: Could not read file: {e}\n")
            outfile.write(f"\n{end_tag}{'-' * (LINE_WIDTH - len(end_tag))}\n")
            outfile.write(f"{SEPARATOR_LINE}\n\n")

            print_progress_bar(i + 1, total_files_to_process, prefix='Progress:', suffix='Completed', length=50)

    print(f"\n{Colors.BLUE}=======================================================================")
    print(f"{Colors.CYAN}  SNAPSHOT FINISHED")
    print(f"{Colors.GREEN}  Total files processed: {total_files_to_process}")
    print(f"{Colors.YELLOW}  Output file: {output_filename}")
    print(f"{Colors.BLUE}=======================================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a code snapshot from a project directory.')
    parser.add_argument('--limit', type=int, default=-1,
                        help='Limit the number of files to process for a quick test run.')
    args = parser.parse_args()

    if not os.path.exists("output"):
        os.makedirs("output")

    generate_code_snapshot(config_path="config.json", limit=args.limit)